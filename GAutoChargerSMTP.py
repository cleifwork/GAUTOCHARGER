import os
import time
import psutil
import logging
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging.handlers import TimedRotatingFileHandler

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
    
logger.addHandler(file_handler)   # Log to file (with timestamp)
logger.addHandler(console_handler)  # Log to console (without timestamp)
logger.setLevel(logging.DEBUG)    # Set logging level to DEBUG

# Utility functions for logging
def log_to_file(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

# Function to read Gmail credentials
def read_gmail_credentials(config_path):
    try:
        with open(config_path, 'r') as config_file:
            credentials = {
                key.strip(): value.strip()
                for line in config_file if '=' in line
                for key, value in [line.split('=', 1)]
            }
        return credentials['gmail'], credentials['appass']
    except KeyError as e:
        logger.error(f"Missing key in credentials file {config_path}: {e}")
        raise
    except FileNotFoundError:
        logger.error(f"Config file '{config_path}' not found.")
        raise
    except Exception as e:
        logger.error(f"Error reading credentials from {config_path}: {e}")
        raise

# Function to send email
def send_email(subject, body, to_email):
    log_msg_success = "Email sent successfully to "
    log_msg_error = "Error sending email: "
    log_msg_unexpected_error = "An unexpected error occurred: "

    try:
        # Path to g_creds.config in the current working directory
        config_path = os.path.join(os.getcwd(), 'g_creds.config')

        # Read Gmail credentials from config file
        gmail_user, app_password = read_gmail_credentials(config_path)

        # Gmail SMTP configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # TLS port

        # Create the email message
        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(gmail_user, app_password)
            server.sendmail(gmail_user, to_email, message.as_string())
            server.quit()

            # Log success
            logger.info(f"{log_msg_success}{to_email}")
        except Exception as e:
            # Log SMTP-related errors
            logger.error(f"{log_msg_error}{e}")
    except Exception as e:
        # Log unexpected errors
        logger.critical(f"{log_msg_unexpected_error}{e}")

# Function to read configuration
def read_config(file_path):
    default_config = {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}

    try:
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

    missing_keys = [key for key in default_config if key not in config]
    if missing_keys:
        log_error(f"Missing required configuration keys {missing_keys} in {file_path}. Using default values.")
        return default_config

    return config

# Function to check the battery and decide on Tapo plug action
async def check_battery_and_control_plug(config):
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
            logger.info(log_message)

            if percent <= config['battery_level_ON'] and not plugged:
                send_email("#PCBatteryLOW", "", "trigger@applet.ifttt.com")
            elif percent >= config['battery_level_OFF'] and plugged:
                send_email("#PCBatteryGOOD", "", "trigger@applet.ifttt.com")
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
