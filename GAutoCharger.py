import os
import time
import psutil
import logging
import asyncio
from tapo import ApiClient
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
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 180}
    except ValueError as e:
        log_error(f"Error parsing values in '{file_path}': {e}. Ensure all values are valid integers. Using default values.")
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 180}
    except Exception as e:
        log_error(f"Unexpected error while reading '{file_path}': {e}. Using default values.")
        return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 180}

    # Ensure all required config values are present
    required_keys = ['battery_level_ON', 'battery_level_OFF', 'plug_control_frequency']
    for key in required_keys:
        if key not in config:
            log_error(f"Missing required configuration '{key}' in {file_path}. Using default values.")
            return {'battery_level_ON': 20, 'battery_level_OFF': 90, 'plug_control_frequency': 180}
    
    return config

# Read credentials from the text file
def read_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key] = value
    except FileNotFoundError:
        log_error(f"Credentials file '{file_path}' not found. Exiting program.")
        exit(1)
    return credentials

# Ensure credentials are available
creds = read_credentials("tapo_creds.config")

tapo_username = creds.get("username")
tapo_password = creds.get("password")
ip_address = creds.get("ip_address")

if not tapo_username or not tapo_password or not ip_address:
    log_error("Missing TAPO credentials or IP address in the tapo_creds.txt file. Exiting program.")
    exit(1)

# Modify get_plug_state to log the device info and not print it to the console
async def get_plug_state(retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            client = ApiClient(tapo_username, tapo_password)
            device = await client.p100(ip_address)
            device_info = await device.get_device_info()

            # Log the device info instead of printing it to the console
            log_to_file(f"Device Info: {device_info}")

            # Return the actual state from device_info
            return device_info.device_on  # Adjust according to actual device_info structure
        except Exception as e:
            attempt += 1
            log_error(f"Error getting plug state (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                print_to_console(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                log_error("Failed to get plug state after multiple attempts. Exiting program.")
                exit(1)  # Exit if all retries fail

# Retry mechanism for the plug control
async def control_plug(action, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            client = ApiClient(tapo_username, tapo_password)
            device = await client.p100(ip_address)
            current_state = await get_plug_state()

            # Wait for 2 seconds before sending the command
            await asyncio.sleep(2)

            if action == "on" and not current_state:
                await device.on()
                print_to_console("Tapo P100 turned on (Battery low)")
                log_to_file("Tapo P100 turned on (Battery low)")
            elif action == "off" and current_state:
                await device.off()
                print_to_console("Tapo P100 turned off (Battery good)")
                log_to_file("Tapo P100 turned off (Battery good)")
            return  # Exit the function on success
        except Exception as e:
            attempt += 1
            log_error(f"Error controlling plug (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                print_to_console(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                log_error("Failed to control plug after multiple attempts. Exiting program.")
                exit(1)  # Exit if all retries fail

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
                await control_plug("on")  # Turn on the plug
            elif percent >= config['battery_level_OFF'] and plugged:
                await control_plug("off")  # Turn off the plug
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
