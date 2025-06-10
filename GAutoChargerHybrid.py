import os
import time
import psutil
import logging
import asyncio
import base64
from logging.handlers import TimedRotatingFileHandler
from email.mime.text import MIMEText

# --- Tapo Local API Imports ---
try:
    from tapo import ApiClient
except ImportError:
    # Log error if tapo is not installed, but allow script to run for remote control
    print("Warning: 'tapo' library not found. Local control will not be available. Please install it using 'pip install tapo-p100-api'.")
    ApiClient = None # Set to None if not available

# --- Google OAuth2 & Gmail API Imports ---
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    # Log error if Google API libs are not installed, but allow script to run for local control
    print("Warning: Google API libraries not found. Remote (IFTTT) control will not be available. Please install 'google-auth-oauthlib', 'google-api-python-client'.")
    Credentials, InstalledAppFlow, Request, build = None, None, None, None


# --- Configuration and Logging Setup ---

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

log_file_path = "logs/script_log.txt"

# Create a TimedRotatingFileHandler (for file logging)
file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
file_handler.suffix = "%Y%m%d"
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create a StreamHandler (for console logging)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) # Log everything to the file

# Clear existing handlers to avoid duplicate logs if run multiple times in same process
if logger.hasHandlers():
    logger.handlers.clear()

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Set different log levels for file and console
console_handler.setLevel(logging.INFO) # Only show INFO+ messages directly in console

# Custom filter to provide hints in console but keep full logs in file (from your VPN script)
class ConsoleFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.DEBUG:
            record.msg = "DEBUG Log Found (See log file for details)"
        elif record.levelno == logging.WARNING:
            record.msg = "WARNING Log Found (See log file for details)"
        elif record.levelno == logging.ERROR:
            record.msg = "ERROR Log Found (See log file for details)"
        elif record.levelno == logging.CRITICAL:
            record.msg = "CRITICAL Log Found (See log file for details)"
        return True

console_handler.addFilter(ConsoleFilter())


# Utility functions for logging
def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_debug(message):
    logger.debug(message)


# --- Configuration and Credential Reading ---

# Function to read general configuration (battery levels, frequency)
def read_config(file_path):
    default_config = {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}
    ideal_battery_low_range = (10, 50)
    ideal_battery_good_range = (51, 100)

    config = default_config.copy() # Start with defaults

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key in default_config: # Only process expected keys
                        try:
                            config[key] = int(value)
                        except ValueError:
                            log_error(f"Invalid integer value for '{key}' in '{file_path}'. Using default.")
    except FileNotFoundError:
        log_error(f"Config file '{file_path}' not found. Using default values.")
    except Exception as e:
        log_error(f"Unexpected error while reading '{file_path}': {e}. Using default values.")

    # Validate `battery_level_ON` range
    if not (ideal_battery_low_range[0] <= config['battery_level_ON'] <= ideal_battery_low_range[1]):
        log_error(f"'battery_level_ON' ({config['battery_level_ON']}) must be between {ideal_battery_low_range[0]} and {ideal_battery_low_range[1]}. Default value {default_config['battery_level_ON']} will be used.")
        config['battery_level_ON'] = default_config['battery_level_ON']

    # Validate `battery_level_OFF` range
    if not (ideal_battery_good_range[0] <= config['battery_level_OFF'] <= ideal_battery_good_range[1]):
        log_error(f"'battery_level_OFF' ({config['battery_level_OFF']}) must be between {ideal_battery_good_range[0]} and {ideal_battery_good_range[1]}. Default value {default_config['battery_level_OFF']} will be used.")
        config['battery_level_OFF'] = default_config['battery_level_OFF']

    # Validate logical relationship
    if config['battery_level_ON'] >= config['battery_level_OFF']:
        log_error(f"'battery_level_ON' ({config['battery_level_ON']}) cannot be greater than or equal to 'battery_level_OFF' ({config['battery_level_OFF']}). Default values will be used.")
        config['battery_level_ON'] = default_config['battery_level_ON']
        config['battery_level_OFF'] = default_config['battery_level_OFF']

    return config

# Function to read Tapo credentials
def read_tapo_credentials(file_path="tapo_creds.config"):
    creds = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    creds[key] = value
    except FileNotFoundError:
        log_error(f"Tapo credentials file '{file_path}' not found. Local Tapo control will not be available.")
        return None
    except Exception as e:
        log_error(f"Error reading Tapo credentials from '{file_path}': {e}. Local Tapo control may fail.")
        return None

    if not all(k in creds for k in ["username", "password", "ip_address"]):
        log_error("Missing 'username', 'password', or 'ip_address' in tapo_creds.config. Local Tapo control will not be available.")
        return None
    return creds


# --- Tapo Local Control Functions ---

async def get_tapo_plug_state(tapo_creds, retries=1, delay=2): # Reduced retries for quicker fallback
    if not ApiClient or not tapo_creds:
        log_debug("Tapo API client not available or credentials missing. Cannot get local plug state.")
        return None # Indicate inability to get state locally

    attempt = 0
    while attempt < retries:
        try:
            client = ApiClient(tapo_creds["username"], tapo_creds["password"])
            device = await client.p100(tapo_creds["ip_address"])
            device_info = await device.get_device_info()
            log_debug(f"Tapo Device Info (Local): {device_info}")
            return device_info.device_on
        except Exception as e:
            attempt += 1
            log_debug(f"Error getting local Tapo plug state (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    log_error("Failed to get local Tapo plug state after multiple attempts.")
    return None # Indicate failure after retries


async def control_tapo_plug(action, tapo_creds, retries=3, delay=2):
    if not ApiClient or not tapo_creds:
        log_debug("Tapo API client not available or credentials missing. Cannot control local plug.")
        return False # Indicate failure

    attempt = 0
    while attempt < retries:
        try:
            client = ApiClient(tapo_creds["username"], tapo_creds["password"])
            device = await client.p100(tapo_creds["ip_address"])
            
            # Get current state to avoid unnecessary commands
            current_state = await get_tapo_plug_state(tapo_creds, retries=1) # Get state without causing full control retry loop
            if current_state is None: # Failed to get state, assume cannot control
                log_error("Could not determine current Tapo plug state locally. Skipping local control attempt.")
                return False

            if action == "on" and not current_state:
                await device.on()
                log_info("Tapo P100 turned on locally.")
                return True # Success
            elif action == "off" and current_state:
                await device.off()
                log_info("Tapo P100 turned off locally.")
                return True # Success
            else:
                log_info(f"Tapo P100 already in desired state ('{action}'). No action taken locally.")
                return True # Already in desired state is also a success
        except Exception as e:
            attempt += 1
            log_debug(f"Error controlling local Tapo plug (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    log_error(f"Failed to control local Tapo plug to '{action}' after multiple attempts.")
    return False # Indicate failure


# --- Gmail API (IFTTT Remote Control) Functions ---

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials.json"

def get_gmail_service():
    """Authenticate and return a Gmail API service instance with proper token refreshing."""
    if not Credentials or not InstalledAppFlow or not Request or not build:
        log_debug("Google API libraries not imported. Cannot get Gmail service.")
        return None

    creds = None

    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            log_error(f"Error loading token from '{TOKEN_PATH}': {e}. Will attempt re-authentication.")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                log_info("Refreshing Gmail API token...")
                creds.refresh(Request())
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
                log_info("Gmail API token refreshed successfully.")
            except Exception as e:
                log_error(f"Gmail API token refresh failed: {e}. Re-authenticating...")
                creds = None
        
        if not creds: # If no creds or refresh failed
            if not os.path.exists(CREDENTIALS_PATH):
                log_error(f"Google client secrets file '{CREDENTIALS_PATH}' not found. Cannot authenticate for Gmail API. Remote control not available.")
                return None
            try:
                log_info("Performing full Gmail API OAuth2 authentication. Please follow the browser prompts.")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
                log_info("Gmail API authentication successful.")
            except Exception as e:
                log_error(f"Error during Gmail API OAuth2 authentication: {e}. Remote control not available.")
                return None
    
    if creds:
        try:
            return build("gmail", "v1", credentials=creds)
        except Exception as e:
            log_error(f"Error building Gmail service: {e}. Remote control not available.")
            return None
    return None


def send_ifttt_email(subject, to_email="trigger@applet.ifttt.com"):
    """Send an email using Gmail API to trigger IFTTT."""
    service = get_gmail_service()
    if not service:
        log_error("Gmail service not available. Cannot send IFTTT email.")
        return False

    try:
        message = MIMEText("") # Body can be empty for IFTTT trigger
        message["to"] = to_email
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        log_info(f"IFTTT email sent successfully with subject: '{subject}'")
        return True
    except Exception as e:
        log_error(f"Error sending IFTTT email: {e}")
        return False


# --- Hybrid Plug Control Logic ---

async def control_plug_hybrid(action, config, tapo_creds):
    """
    Attempts to control the plug locally first, then falls back to remote control via IFTTT.
    Returns True if control attempt was successful (either local or remote), False otherwise.
    """
    log_info(f"Attempting to control plug to '{action}' state...")

    # 1. Attempt Local Control (Tapo API)
    if tapo_creds:
        log_info("Trying local Tapo plug control...")
        local_success = await control_tapo_plug(action, tapo_creds)
        if local_success:
            log_info("Local Tapo plug control successful.")
            return True
        else:
            log_warning("Local Tapo plug control failed. Falling back to remote control via IFTTT.")
    else:
        log_warning("Tapo credentials not loaded or Tapo API client missing. Skipping local control.")

    # 2. Fallback to Remote Control (IFTTT via Gmail API)
    if action == "on":
        subject = "#PCBatteryLOW"
    elif action == "off":
        subject = "#PCBatteryGOOD"
    else:
        log_error(f"Invalid action for remote control: {action}")
        return False

    log_info(f"Trying remote control via IFTTT email with subject: '{subject}'...")
    remote_success = send_ifttt_email(subject)
    if remote_success:
        log_info("Remote control via IFTTT email successful.")
        return True
    else:
        log_error("Remote control via IFTTT email failed.")
        return False


# --- Main Battery Check and Loop ---

async def check_battery_and_control_plug(config, tapo_creds):
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            log_info(f"Battery Level: {percent}% - Plugged In: {plugged}")

            if percent <= config['battery_level_ON'] and not plugged:
                log_info(f"Battery is LOW ({percent}% <= {config['battery_level_ON']}%). Attempting to turn ON charger.")
                await control_plug_hybrid("on", config, tapo_creds)
            elif percent >= config['battery_level_OFF'] and plugged:
                log_info(f"Battery is GOOD ({percent}% >= {config['battery_level_OFF']}%). Attempting to turn OFF charger.")
                await control_plug_hybrid("off", config, tapo_creds)
            else:
                log_debug("Battery level within optimal range or state not requiring action. No change needed.")
        else:
            log_error("Battery information not available from psutil.")
    except Exception as e:
        log_error(f"Error in check_battery_and_control_plug: {e}")


async def main():
    # Load config values
    config = read_config("battery_level.config")
    if not config:
        log_error("Failed to load valid configuration. Exiting.")
        return

    # Load Tapo credentials once
    tapo_creds = read_tapo_credentials("tapo_creds.config")
    if not tapo_creds:
        log_warning("Tapo credentials not found or invalid. Local control will not be available. Relying on remote (IFTTT) only.")

    last_check_time = time.time()
    last_print_time = time.time()

    log_info("AutoCharge Hybrid script started. Monitoring battery levels...")

    while True:
        current_time = time.time()

        # Check battery and control plug based on the config's control frequency
        if current_time - last_check_time >= config['plug_control_frequency']:
            await check_battery_and_control_plug(config, tapo_creds)
            last_check_time = current_time

        # Print battery level and plugged status every 20 seconds
        if current_time - last_print_time >= 20:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    plugged = battery.power_plugged
                    log_info(f"Current Status: Battery Level: {percent}% - Plugged In: {plugged}")
                last_print_time = current_time
            except Exception as e:
                log_error(f"Error printing battery status: {e}")

        await asyncio.sleep(1) # Sleep for 1 second to avoid excessive CPU usage

if __name__ == "__main__":
    # Ensure event loop is clean for re-runs in some environments (like Jupyter)
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot run a second event loop" in str(e):
            log_warning("Asyncio event loop already running. Using existing loop.")
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
