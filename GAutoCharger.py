import os
import psutil
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import asyncio
from tapo import ApiClient

# Function to read credentials from the text file
def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key] = value
    return credentials

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging with TimedRotatingFileHandler
log_file_path = "logs/script_log.txt"
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
handler.suffix = "%Y%m%d%H%M%S"  # Append timestamp to rotated files
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

# Read credentials from the text file
creds = read_credentials("tapo_creds.txt")

# Ensure credentials are available
tapo_username = creds.get("username")
tapo_password = creds.get("password")
ip_address = creds.get("ip_address")

if not tapo_username or not tapo_password or not ip_address:
    raise ValueError("Missing TAPO credentials or IP address in the tapo_creds.txt file.")

# Print and log utility functions
def print_to_console(message):
    print(message)

def log_to_file(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

# Async function to get the current state of the Tapo plug
async def get_plug_state():
    try:
        client = ApiClient(tapo_username, tapo_password)
        device = await client.p100(ip_address)
        device_info = await device.get_device_info()
        
        # Print the device_info to understand its structure
        print("Device Info:", device_info)
        
        # Return the actual state from device_info
        return device_info.device_on  # Adjust according to actual device_info structure
    except Exception as e:
        log_error(f"Error getting plug state: {e}")
        raise

# Async function to control the Tapo plug
async def control_plug(action):
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
            print_to_console("Tapo P100 turned off (Battery full)")
            log_to_file("Tapo P100 turned off (Battery full)")
    except Exception as e:
        log_error(f"Error controlling plug: {e}")
        raise

# Function to check the battery and decide on Tapo plug action
async def check_battery_and_control_plug():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged

            # Log the battery status
            log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
            log_to_file(log_message)  # Log to file

            # Control the plug based on battery level
            if percent <= 20 and not plugged:
                await control_plug("on")  # Turn on the plug
            elif percent >= 90 and not plugged:
                await control_plug("off")  # Turn off the plug
        else:
            message = "Battery information not available."
            print_to_console(message)
            log_to_file(message)
    except Exception as e:
        log_error(f"Error checking battery and controlling plug: {e}")

# Main async loop
async def main():
    last_check_time = time.time()
    last_print_time = time.time()

    while True:
        current_time = time.time()
        
        # Check battery and control plug every 2 minutes (120 seconds)
        if current_time - last_check_time >= 300:
            await check_battery_and_control_plug()
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

#############################################################################################

# import psutil
# import time
# import logging
# import asyncio
# from tapo import ApiClient

# # Function to read credentials from the text file
# def read_credentials(file_path):
#     credentials = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             if '=' in line:
#                 key, value = line.strip().split('=', 1)
#                 credentials[key] = value
#     return credentials

# # Configure logging
# logging.basicConfig(filename="script_log.txt", level=logging.INFO,
#                     format='%(asctime)s - %(message)s')

# # Read credentials from the text file
# creds = read_credentials("tapo_creds.txt")

# # Ensure credentials are available
# tapo_username = creds.get("username")
# tapo_password = creds.get("password")
# ip_address = creds.get("ip_address")

# if not tapo_username or not tapo_password or not ip_address:
#     raise ValueError("Missing TAPO credentials or IP address in the tapo_creds.txt file.")

# # Print and log utility functions
# def print_to_console(message):
#     print(message)

# def log_to_file(message):
#     logging.info(message)

# def log_error(message):
#     logging.error(message)

# # Async function to get the current state of the Tapo plug
# async def get_plug_state():
#     client = ApiClient(tapo_username, tapo_password)
#     device = await client.p100(ip_address)
#     device_info = await device.get_device_info()
    
#     # Print the device_info to understand its structure
#     print("Device Info:", device_info)
    
#     # Update this line based on the actual structure of device_info
#     # For example, if device_info has a method or attribute to get the state, use it here
#     return device_info.device_on  # Adjust according to actual device_info structure

# # Async function to control the Tapo plug
# async def control_plug(action):
#     try:
#         client = ApiClient(tapo_username, tapo_password)
#         device = await client.p100(ip_address)
#         current_state = await get_plug_state()

#         # Wait for 2 seconds before sending the command
#         await asyncio.sleep(2)

#         if action == "on" and not current_state:
#             await device.on()
#             print_to_console("Tapo P100 turned on (Battery low)")
#             log_to_file("Tapo P100 turned on (Battery low)")
#         elif action == "off" and current_state:
#             await device.off()
#             print_to_console("Tapo P100 turned off (Battery full)")
#             log_to_file("Tapo P100 turned off (Battery full)")
#     except Exception as e:
#         log_error(f"Error controlling plug: {e}")
#         raise

# # Function to check the battery and decide on Tapo plug action
# async def check_battery_and_control_plug():
#     try:
#         battery = psutil.sensors_battery()
#         if battery:
#             percent = battery.percent
#             plugged = battery.power_plugged

#             # Log the battery status
#             log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
#             log_to_file(log_message)  # Log to file

#             # Control the plug based on battery level
#             if percent <= 45 and not plugged:
#                 await control_plug("on")  # Turn on the plug
#             elif percent >= 100 and not plugged:
#                 await control_plug("off")  # Turn off the plug
#         else:
#             message = "Battery information not available."
#             print_to_console(message)
#             log_to_file(message)
#     except Exception as e:
#         log_error(f"Error checking battery and controlling plug: {e}")

# # Main async loop
# async def main():
#     last_check_time = time.time()
#     last_print_time = time.time()

#     while True:
#         current_time = time.time()
        
#         # Check battery and control plug every 2 minutes (120 seconds)
#         if current_time - last_check_time >= 120:
#             await check_battery_and_control_plug()
#             last_check_time = current_time

#         # Print battery level and plugged status every 20 seconds
#         if current_time - last_print_time >= 20:
#             try:
#                 battery = psutil.sensors_battery()
#                 if battery:
#                     percent = battery.percent
#                     plugged = battery.power_plugged
#                     log_message = f"Battery Level: {percent}% - Plugged In: {plugged}"
#                     print_to_console(log_message)
#                     log_to_file(log_message)
#                 last_print_time = current_time
#             except Exception as e:
#                 log_error(f"Error printing battery status: {e}")

#         await asyncio.sleep(1)  # Sleep for 1 second to avoid excessive CPU usage

# # Entry point to start the asyncio loop
# if __name__ == "__main__":
#     asyncio.run(main())