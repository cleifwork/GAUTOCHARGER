import os
import time
import psutil
import logging
import asyncio
import base64
from logging.handlers import TimedRotatingFileHandler
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Directory where logs will be saved
log_file_path = "logs/script_log.txt"

# Create a TimedRotatingFileHandler (for file logging)
file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
file_handler.suffix = "%Y%m%d"  # Format for rotated log filenames
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Includes timestamp
file_handler.setFormatter(file_formatter)

# Create a StreamHandler (for console logging)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(levelname)s - %(message)s')  # No timestamp for console logs
console_handler.setFormatter(console_formatter)

# Configure the root logger
logger = logging.getLogger()

# Clear existing handlers to avoid duplicate logs
if logger.hasHandlers():
    logger.handlers.clear()
    
# Add handlers
logger.addHandler(file_handler)   # Log everything to the file
logger.addHandler(console_handler)  # Log only INFO and above to the console

# Set different log levels for file and console
logger.setLevel(logging.DEBUG)  # Log everything to file
console_handler.setLevel(logging.INFO)  # Only show INFO+ logs in console

# Suppress DEBUG logs from external libraries (googleapiclient, urllib3, etc.)
logging.getLogger("googleapiclient").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# Utility functions for logging
def log_to_file(message):
    logger.info(message)


def log_error(message):
    logger.error(message)

# Gmail API setup
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    """Authenticate and return a Gmail API service instance."""
    creds = None
    token_path = "token.json"  # Path for storing the OAuth token

    # Load existing credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh token if expired, otherwise request a new one
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Refresh token if expired
            except Exception as e:
                logging.error(f"Token refresh failed: {e}. Re-authenticating...")
                creds = None  # Force re-authentication
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email(subject, body, to_email):
    """Send an email using Gmail API."""
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message["to"] = to_email
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        logging.info(f"Email sent successfully to IFTTT")
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return False
      
      
# Function to read configuration
def read_config(file_path):
    # Default configuration values
    default_config = {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}

    # Ideal ranges for battery levels
    ideal_battery_low_range = (10, 50)  # Ideal range for battery_level_ON
    ideal_battery_good_range = (51, 100)  # Ideal range for battery_level_OFF

    try:
        # Parse the configuration file
        with open(file_path, 'r') as file:
            config = {
                key: int(value)
                for line in file
                if '=' in line
                for key, value in [line.strip().split('=', 1)]
            }
    except FileNotFoundError:
        log_error(f"Config file '{file_path}' not found. Using default values.")
        return default_config
    except ValueError as e:
        log_error(f"Error parsing values in '{file_path}': {e}. Using default values.")
        return default_config
    except Exception as e:
        log_error(f"Unexpected error while reading '{file_path}': {e}. Using default values.")
        return default_config

    # Validate `battery_level_ON` range
    if not (ideal_battery_low_range[0] <= config['battery_level_ON'] <= ideal_battery_low_range[1]):
        log_error(f"'battery_level_ON' ({config['battery_level_ON']}) must be between {ideal_battery_low_range[0]} and {ideal_battery_low_range[1]}. Default value {default_config['battery_level_ON']} will be used.")
        config['battery_level_ON'] = default_config['battery_level_ON']

    # Validate `battery_level_OFF` range
    if not (ideal_battery_good_range[0] <= config['battery_level_OFF'] <= ideal_battery_good_range[1]):
        log_error(f"'battery_level_OFF' ({config['battery_level_OFF']}) must be between {ideal_battery_good_range[0]} and {ideal_battery_good_range[1]}. Default value {default_config['battery_level_OFF']} will be used.")
        config['battery_level_OFF'] = default_config['battery_level_OFF']

    # Validate logical relationship between `battery_level_ON` and `battery_level_OFF`
    if config['battery_level_ON'] >= config['battery_level_OFF']:
        log_error(f"'battery_level_ON' ({config['battery_level_ON']}) cannot be greater than or equal to 'battery_level_OFF' ({config['battery_level_OFF']}). Default values will be used.")
        config['battery_level_ON'] = default_config['battery_level_ON']
        config['battery_level_OFF'] = default_config['battery_level_OFF']

    # Return validated configuration
    return config


async def check_battery_and_control_plug(config):
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
            logger.info(log_message)
            
            # Condition for turning ON charger
            if percent <= config['battery_level_ON'] and not plugged:
                if send_email("#PCBatteryLOW", "", "trigger@applet.ifttt.com"):
                    logger.info("Laptop Charger --> Turning ON...")  # ✅ Only log if email was sent successfully

            # Condition for turning OFF charger
            elif percent >= config['battery_level_OFF'] and plugged:
                if send_email("#PCBatteryGOOD", "", "trigger@applet.ifttt.com"):
                    logger.info("Laptop Charger --> Turning OFF...")  # ✅ Only log if email was sent successfully

        else:
            log_error("Battery information not available.")
    except Exception as e:
        log_error(f"Error checking battery and controlling plug: {e}")


# Main async loop
async def main():
    try:
        config = read_config("battery_level.config")
    except (FileNotFoundError, ValueError) as e:
        log_error(str(e))
        return

    last_check_time = time.time()
    last_print_time = time.time()

    while True:
        current_time = time.time()

        if current_time - last_check_time >= config['plug_control_frequency']:
            await check_battery_and_control_plug(config)
            last_check_time = current_time

        if current_time - last_print_time >= 20:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    plugged = battery.power_plugged
                    logger.info(f"Battery Level: {percent}% - Plugged In: {plugged}")
                last_print_time = current_time
            except Exception as e:
                log_error(f"Error printing battery status: {e}")

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())