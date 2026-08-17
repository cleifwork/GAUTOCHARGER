import os
import json
import utils
import base64
import psutil
import logging
import asyncio
import platform
import subprocess
import time
from logging.handlers import TimedRotatingFileHandler
from email.mime.text import MIMEText

# --- Tapo Local API Imports ---
try:
    from tapo import ApiClient
except ImportError:
    print("Warning: 'tapo' library not found. Local control will not be available. Please install it using 'pip install tapo-p100-api'.")
    ApiClient = None

# --- Google OAuth2 & Gmail API Imports ---
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    print("Warning: Google API libraries not found. Home Assistant email fallback will not be available.")
    Credentials, InstalledAppFlow, Request, build = None, None, None, None

# --- Configuration and Constants from utils.py ---
LOGS_DIR = os.path.join(utils.exe_dir, "logs")
LOCK_FILE = os.path.join(utils.exe_dir, "autocharge_script.lock") # This path was not in utils, so we construct it
STATE_FILE = utils.FILE_PATHS["autocharge_state"]
CONFIG_FILE = utils.FILE_PATHS["battery_level"]
TAPO_CREDS_FILE = utils.FILE_PATHS["tapo_creds"]
HOME_ASSISTANT_EMAIL_CONFIG_FILE = utils.FILE_PATHS["home_assistant_email"]
GMAIL_TOKEN_PATH = utils.FILE_PATHS["tokens"]
GMAIL_CREDS_PATH = utils.FILE_PATHS["creds"]
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# After the initial fallback email, retry at 10, 30, and 90 minutes, then once
# every two hours while the same action is still required.
DEFAULT_EMAIL_RETRY_DELAYS_MINUTES = (10, 20, 60)
DEFAULT_EMAIL_REPEAT_RETRY_MINUTES = 120


# --- Logging Setup ---
def setup_logging():
    """Sets up file and console logging."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    log_file_path = os.path.join(LOGS_DIR, "script_log.txt")
    
    logger = logging.getLogger()
    
    # ### FIX: Clear handlers only if they have been configured in a previous run of this function
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    # File handler for detailed logs with timestamps
    file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
    file_handler.suffix = "%Y%m%d"
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler for high-level info without timestamps
    console_handler = logging.StreamHandler()
    # ### FIX: Changed console formatter to remove the timestamp for a cleaner output.
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# --- Lock File and State Management ---

def create_lock_file():
    """Checks for lock file and prompts for deletion if it exists."""
    if os.path.exists(LOCK_FILE):
        print("\nLock file 'autocharge_script.lock' already exists.")
        response = input("Do you want to delete it and proceed? (Y/n): ").strip().lower()
        if response == 'y' or response == 'yes':
            try:
                os.remove(LOCK_FILE)
                logger.info("Existing lock file deleted by user.")
            except Exception as e:
                logger.error(f"Failed to delete lock file: {e}")
                return False
        else:
            logger.warning("User chose not to delete the lock file. Exiting.")
            return False

    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        logger.info("Lock file created.")
        return True
    except Exception as e:
        logger.error(f"Failed to create lock file: {e}")
        return False

def remove_lock_file():
    """Removes the lock file on clean exit."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        logger.info("Lock file removed.")

def load_state():
    """Loads the last known state from a JSON file."""
    default_state = {
        "last_action": "unknown",
        "active_action": None,
        "last_local_success_action": "unknown",
        "last_confirmed_action": "unknown",
        "email_fallback": {
            "action": None,
            "attempt_count": 0,
            "last_attempt_at": None,
        },
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                loaded_state = json.load(f)
                if isinstance(loaded_state, dict):
                    default_state.update(loaded_state)
                    fallback_state = default_state.get("email_fallback")
                    if not isinstance(fallback_state, dict):
                        fallback_state = {}
                    default_state["email_fallback"] = {
                        "action": fallback_state.get("action"),
                        "attempt_count": fallback_state.get("attempt_count", 0),
                        "last_attempt_at": fallback_state.get("last_attempt_at"),
                    }
                    return default_state
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error reading state file {STATE_FILE}: {e}. Starting with a fresh state.")
    return default_state

def save_state(state):
    """Saves the current state to a JSON file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
    except IOError as e:
        logger.error(f"Could not write to state file {STATE_FILE}: {e}")

# --- Configuration Reading ---
def read_config(file_path):
    """Reads and validates the main configuration file."""
    default_config = {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}
    config = default_config.copy()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key in default_config:
                        try:
                            config[key] = int(value)
                        except ValueError:
                            logger.error(f"Invalid integer for '{key}' in '{file_path}'. Using default.")
    except FileNotFoundError:
        logger.error(f"Config file '{file_path}' not found. Using defaults.")

    # Validation
    if not (10 <= config['battery_level_ON'] <= 50):
        logger.error(f"battery_level_ON ({config['battery_level_ON']}) out of range (10-50). Reverting to default.")
        config['battery_level_ON'] = default_config['battery_level_ON']
    if not (51 <= config['battery_level_OFF'] <= 100):
        logger.error(f"battery_level_OFF ({config['battery_level_OFF']}) out of range (51-100). Reverting to default.")
        config['battery_level_OFF'] = default_config['battery_level_OFF']
    if config['battery_level_ON'] >= config['battery_level_OFF']:
        logger.error("battery_level_ON must be less than battery_level_OFF. Reverting to defaults.")
        config['battery_level_ON'] = default_config['battery_level_ON']
        config['battery_level_OFF'] = default_config['battery_level_OFF']
    return config

def read_tapo_credentials(file_path):
    """Reads Tapo credentials."""
    creds = {}
    if not os.path.exists(file_path):
        logger.warning(f"Tapo credentials file '{file_path}' not found. Local control disabled.")
        return None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                    creds[key] = value
        if not all(k in creds for k in ["username", "password", "ip_address"]):
            logger.error("Missing credentials in tapo_creds.config. Local control disabled.")
            return None
        return creds
    except Exception as e:
        logger.error(f"Error reading Tapo credentials from '{file_path}': {e}.")
        return None

def read_home_assistant_email_config(file_path):
    """Reads the recipient and Home Assistant email command subjects."""
    required_keys = {"to_email", "on_subject", "off_subject"}
    config = {}

    if not os.path.exists(file_path):
        logger.warning(
            f"Home Assistant email config '{file_path}' not found. "
            "Remote email fallback is disabled."
        )
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = map(str.strip, line.split('=', 1))
                    config[key] = value
    except OSError as e:
        logger.error(f"Unable to read Home Assistant email config '{file_path}': {e}")
        return None

    missing_keys = sorted(key for key in required_keys if not config.get(key))
    if missing_keys:
        logger.error(
            "Home Assistant email fallback is disabled; missing config value(s): "
            f"{', '.join(missing_keys)}."
        )
        return None

    # Prevent a malformed config value from injecting extra email headers.
    for key in ("to_email", "on_subject", "off_subject"):
        if '\\r' in config[key] or '\\n' in config[key]:
            logger.error(f"Home Assistant email fallback is disabled; '{key}' contains a newline.")
            return None

    retry_delays_value = config.get("retry_delays_minutes", "10,20,60")
    try:
        retry_delays = tuple(
            int(value.strip())
            for value in retry_delays_value.split(",")
            if value.strip()
        )
        if not retry_delays or any(delay <= 0 for delay in retry_delays):
            raise ValueError
        config["retry_delays_minutes"] = retry_delays
    except ValueError:
        logger.error(
            "Invalid retry_delays_minutes. Using default email retry delays: "
            f"{DEFAULT_EMAIL_RETRY_DELAYS_MINUTES}."
        )
        config["retry_delays_minutes"] = DEFAULT_EMAIL_RETRY_DELAYS_MINUTES

    try:
        repeat_retry_minutes = int(
            config.get("repeat_retry_minutes", DEFAULT_EMAIL_REPEAT_RETRY_MINUTES)
        )
        if repeat_retry_minutes <= 0:
            raise ValueError
        config["repeat_retry_minutes"] = repeat_retry_minutes
    except ValueError:
        logger.error(
            "Invalid repeat_retry_minutes. Using default repeat retry delay: "
            f"{DEFAULT_EMAIL_REPEAT_RETRY_MINUTES}."
        )
        config["repeat_retry_minutes"] = DEFAULT_EMAIL_REPEAT_RETRY_MINUTES

    return config

# --- Health Checks and Device Control ---

def ping_host(host):
    """Pings a host to check for connectivity. Returns True if successful."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        # Pinging with a timeout of 1 second (1000 ms for windows)
        timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
        command.extend([timeout_param, '1'])
        return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2).returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

async def control_tapo_plug(action, tapo_creds):
    """Controls the Tapo plug locally with a preceding ping check."""
    if not ApiClient or not tapo_creds:
        return False

    if not ping_host(tapo_creds["ip_address"]):
        logger.warning(f"Tapo plug at {tapo_creds['ip_address']} is not reachable (ping failed).")
        return False

    try:
        client = ApiClient(tapo_creds["username"], tapo_creds["password"])
        device = await asyncio.wait_for(client.p100(tapo_creds["ip_address"]), timeout=5.0)
        
        if action == "on":
            await device.on()
            logger.info("Tapo P100 turned ON locally.")
        elif action == "off":
            await device.off()
            logger.info("Tapo P100 turned OFF locally.")
        return True
    except asyncio.TimeoutError:
        logger.error("Tapo API call timed out after 5 seconds.")
        return False
    except Exception as e:
        logger.error(f"Failed to control local Tapo plug: {e}")
        return False

def get_gmail_service():
    """Authenticates and returns a Gmail API service instance for sending email."""
    if not all([Credentials, InstalledAppFlow, Request, build]):
        return None

    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, GMAIL_SCOPES)
        except Exception as e:
            logger.error(f"Unable to read Gmail OAuth token '{GMAIL_TOKEN_PATH}': {e}")
            return None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Refreshing Gmail OAuth token...")
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Gmail OAuth token refresh failed: {e}")
                return None
        else:
            if not os.path.exists(GMAIL_CREDS_PATH):
                logger.error(f"'{GMAIL_CREDS_PATH}' not found. Cannot authenticate Home Assistant email fallback.")
                return None
            try:
                logger.info("Opening Gmail OAuth authorization for Home Assistant email fallback...")
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDS_PATH, GMAIL_SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logger.error(f"Gmail OAuth authorization failed: {e}")
                return None

        try:
            with open(GMAIL_TOKEN_PATH, "w", encoding="utf-8") as token:
                token.write(creds.to_json())
        except OSError as e:
            logger.error(f"Unable to save Gmail OAuth token: {e}")
            return None

    try:
        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        logger.error(f"Unable to build Gmail API service: {e}")
        return None

def send_home_assistant_email(action, email_config):
    """Sends the configured Home Assistant ON/OFF command through the Gmail API."""
    if not email_config:
        logger.error("Cannot send Home Assistant command: email fallback is not configured.")
        return False

    subject = email_config["on_subject"] if action == "on" else email_config["off_subject"]
    service = get_gmail_service()
    if not service:
        logger.error("Cannot send Home Assistant command: Gmail OAuth service is not available.")
        return False

    try:
        message = MIMEText("")
        message["to"] = email_config["to_email"]
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

        logger.info(f"Home Assistant {action.upper()} command email sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to send Home Assistant {action.upper()} command email: {e}")
        return False

def reset_email_retry_state(state, action=None):
    """Clears fallback-email attempts for a new or locally completed action."""
    state["email_fallback"] = {
        "action": action,
        "attempt_count": 0,
        "last_attempt_at": None,
    }

def email_retry_wait_minutes(email_config, attempt_count):
    """Returns the delay after the given number of email attempts."""
    retry_delays = email_config["retry_delays_minutes"]
    if attempt_count <= len(retry_delays):
        return retry_delays[attempt_count - 1]
    return email_config["repeat_retry_minutes"]

def battery_status_confirms_action(action, plugged):
    """Returns whether Windows' charging status confirms the requested action.

    This is an indirect confirmation: it verifies that the laptop is receiving
    power (or not), rather than querying the Tapo plug itself. It is useful
    when a VPN prevents direct local Tapo access.
    """
    return plugged if action == "on" else not plugged

async def send_home_assistant_email_if_due(action, email_config, state):
    """Sends a rate-limited fallback email and persists every send attempt."""
    if not email_config:
        logger.error("Home Assistant email fallback is not configured.")
        return False

    fallback_state = state["email_fallback"]
    if fallback_state.get("action") != action:
        reset_email_retry_state(state, action)
        fallback_state = state["email_fallback"]

    attempt_count = fallback_state.get("attempt_count", 0)
    last_attempt_at = fallback_state.get("last_attempt_at")
    now = time.time()

    if attempt_count and last_attempt_at is not None:
        wait_minutes = email_retry_wait_minutes(email_config, attempt_count)
        wait_seconds = wait_minutes * 60
        elapsed_seconds = now - last_attempt_at
        if elapsed_seconds < wait_seconds:
            remaining_minutes = max(1, round((wait_seconds - elapsed_seconds) / 60))
            logger.info(
                f"Home Assistant {action.upper()} email fallback is rate-limited. "
                f"Next retry in about {remaining_minutes} minute(s)."
            )
            return False

    # Record failed Gmail API calls too, so a send failure cannot cause an API
    # call on every battery loop.
    fallback_state["attempt_count"] = attempt_count + 1
    fallback_state["last_attempt_at"] = now
    save_state(state)

    logger.warning(
        f"Local control failed. Sending Home Assistant {action.upper()} email "
        f"attempt #{fallback_state['attempt_count']}."
    )
    remote_success = await asyncio.to_thread(send_home_assistant_email, action, email_config)
    if remote_success:
        logger.info("Home Assistant fallback email was accepted by Gmail.")
        state["last_action"] = action
        save_state(state)
    else:
        logger.error("Home Assistant fallback email could not be sent; its retry is also rate-limited.")
    return remote_success

# --- Main Application Logic ---

async def check_battery_and_control_plug(config, tapo_creds, email_config, state):
    """Main logic to check battery and decide on plug action."""
    try:
        battery = psutil.sensors_battery()
        if not battery:
            logger.error("Battery information not available from psutil.")
            return

        percent = battery.percent
        plugged = battery.power_plugged
        plugged_str = "Yes" if plugged else "No"
        logger.info(f"Battery:{percent}%, Plugged:{plugged_str}, LastAction:'{state.get('last_action')}'")

        if percent <= config['battery_level_ON']:
            action = "on"
            logger.info(f"Battery is LOW ({percent}%). ON is required.")
        elif percent >= config['battery_level_OFF']:
            action = "off"
            logger.info(f"Battery is GOOD ({percent}%). OFF is required.")
        else:
            logger.debug("Battery is between thresholds; no plug action is required.")
            return

        if state.get("active_action") != action:
            logger.info(f"Starting a new {action.upper()} control cycle.")
            state["active_action"] = action
            state["last_local_success_action"] = "unknown"
            reset_email_retry_state(state, action)
            save_state(state)

        # Home Assistant email is one-way, but the laptop's charging status is
        # a practical confirmation for this charger setup. Once the observed
        # power state matches the requested action, stop local retries and
        # clear the email retry schedule. If it does not match, the existing
        # slow fallback schedule remains in effect.
        if battery_status_confirms_action(action, plugged):
            if state.get("last_confirmed_action") != action:
                logger.info(
                    f"State correction: laptop charging status confirms plug is {action.upper()}."
                )
                state["last_action"] = action
                state["last_confirmed_action"] = action
                reset_email_retry_state(state, action)
                save_state(state)
            else:
                logger.debug(f"Laptop charging status already confirms {action.upper()}.")
            return

        # A sent email does not confirm the Tapo state. When the observed
        # charging status does not match the requested action, retry local
        # control every loop and let the email fallback keep its slow schedule.
        logger.info(f"Attempting local {action.upper()} control.")
        local_success = await control_tapo_plug(action, tapo_creds)
        if local_success:
            logger.info("Local control was successful.")
            state["last_action"] = action
            state["last_local_success_action"] = action
            state["last_confirmed_action"] = action
            reset_email_retry_state(state, action)
            save_state(state)
            return

        # Local calls retry every loop; fallback emails use their own schedule.
        await send_home_assistant_email_if_due(action, email_config, state)

    except Exception as e:
        logger.error(f"Error in check_battery_and_control_plug: {e}", exc_info=True)

async def main():
    """Main application loop."""
    if not create_lock_file():
        return # Exit if another instance is running

    try:
        config = read_config(CONFIG_FILE)
        tapo_creds = read_tapo_credentials(TAPO_CREDS_FILE)
        email_config = read_home_assistant_email_config(HOME_ASSISTANT_EMAIL_CONFIG_FILE)
        state = load_state()

        logger.info("="*50)
        logger.info("AutoCharge Hybrid Script Started")
        logger.info(f"Config: ON at {config['battery_level_ON']}%, OFF at {config['battery_level_OFF']}%")
        logger.info(f"Check Frequency: {config['plug_control_frequency']} seconds")
        logger.info("="*50)
        
        while True:
            await check_battery_and_control_plug(config, tapo_creds, email_config, state)
            await asyncio.sleep(config['plug_control_frequency'])

    except asyncio.CancelledError:
        logger.info("Script cancellation requested.")
    except Exception as e:
        logger.critical(f"An unhandled exception occurred in main loop: {e}", exc_info=True)
    finally:
        remove_lock_file()
        logger.info("AutoCharge Hybrid script stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user (Ctrl+C). Shutting down.")
