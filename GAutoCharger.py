import os
import time
import psutil
import logging
import asyncio
from AutoMailSMTP import send_email
from logging.handlers import TimedRotatingFileHandler

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Directory where logs will be saved
log_file_path = "logs/script_log.txt"

# Create a TimedRotatingFileHandler
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
handler.suffix = "%Y%m%d"  # The format for the rotated filenames
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# Configure logger
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

# Print and log utility functions
def print_to_console(message):
    print(message)

def log_to_file(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def read_config(file_path):
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = int(value)  # Ensure the values are integers
    except FileNotFoundError:
        log_error(f"Config file '{file_path}' not found. Using default values.")
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}
    except ValueError as e:
        log_error(f"Error parsing values in '{file_path}': {e}. Ensure all values are valid integers. Using default values.")
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}
    except Exception as e:
        log_error(f"Unexpected error while reading '{file_path}': {e}. Using default values.")
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}

    # Ensure all required config values are present
    required_keys = ['battery_level_ON', 'battery_level_OFF', 'plug_control_frequency']
    for key in required_keys:
        if key not in config:
            log_error(f"Missing required configuration '{key}' in {file_path}. Using default values.")
            return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 60}
    
    return config

# Function to check the battery and decide on Tapo plug action
async def check_battery_and_control_plug(config):
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            # Log the battery status
            log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
            log_to_file(log_message)  # Log to file

            # Control the plug based on battery level and config thresholds
            if percent <= config['battery_level_ON'] and not plugged:
                send_email("#PCBatteryLOW", "", "trigger@applet.ifttt.com")  # Turn on the plug
            elif percent >= config['battery_level_OFF'] and plugged:
                send_email("#PCBatteryGOOD", "", "trigger@applet.ifttt.com")  # Turn off the plug
        else:
            message = "Battery information not available."
            print_to_console(message)
            log_to_file(message)
    except Exception as e:
        log_error(f"Error checking battery and controlling plug: {e}")

# Main async loop
async def main():
    # Load config values from the config file
    try:
        config = read_config("battery_level.config")
    except (FileNotFoundError, ValueError) as e:
        log_error(str(e))
        print_to_console(str(e))
        return  # Exit if config cannot be loaded

    last_check_time = time.time()
    last_print_time = time.time()

    while True:
        current_time = time.time()

        # Check battery and control plug based on the config's control frequency
        if current_time - last_check_time >= config['plug_control_frequency']:
            await check_battery_and_control_plug(config)
            last_check_time = current_time

        # Print battery level and plugged status every 20 seconds
        if current_time - last_print_time >= 20:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    plugged = battery.power_plugged
                    log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
                    print_to_console(log_message)
                    log_to_file(log_message)
                last_print_time = current_time
            except Exception as e:
                log_error(f"Error printing battery status: {e}")

        await asyncio.sleep(1)  # Sleep for 1 second to avoid excessive CPU usage

# Entry point to start the asyncio loop
if __name__ == "__main__":
    asyncio.run(main())
