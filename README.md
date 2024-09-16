
> [!IMPORTANT]
> **DO NOT USE JUST YET - STILL UNDER DEVELOPMENT** 

# GAUTOCHARGER-V2: AutoCharging Solution

**GAutoCharger-V2** is a battery management automation solution designed for laptops running Windows OS that function as servers and remain connected to a power source 24/7. This tool intelligently controls the charging process by managing a Tapo Smart Plug (e.g., P100) via Wi-Fi. It ensures that the battery is charged only when necessary, extending battery life and improving overall health by avoiding constant charging cycles.

## Features
- Automated Charging Control: Automatically turns on the smart plug when the battery level is low and turns it off when the battery is full, based on configurable thresholds.
- Battery Level Monitoring: Logs battery levels and power status at regular intervals, providing full visibility into the device’s charging state.
- Smart Plug Integration: Communicates with Tapo Smart Plug through the Tapo API, allowing remote control of the power outlet connected to your laptop’s charger.
- Daily Log Rotation: Generates daily logs stored in the ```/logs/``` directory with automatic log rotation, ensuring minimal maintenance and easy tracking of battery status.
- Resilient Retry Mechanism: Built-in retry logic for handling temporary connection issues with the Tapo Smart Plug.
- Configurable Parameters: Easy-to-set thresholds and other parameters in the ```tapo_creds.txt``` file for quick configuration.

## Requirements
- Python 3.8+
- Tapo Smart Plug (P100, P105, etc.)
- Tapo account with username and password
- psutil: For battery and power status monitoring
- Tapo Python API: For controlling the Tapo Smart Plug
- asyncio: For handling asynchronous operations
- logging: For logging battery status and error messages
- Windows OS (for battery monitoring)


## Demo

-   [GConnect App Demo](https://www.youtube.com/)
-   [GConnect Installation & Configuration](https://www.youtube.com/)

## Authors
- [@cleifwork](https://www.github.com/cleifwork)
## Environment Variables

- To run this project, you will need to add the following environment variables to your **GAUTOCHARGER** folder.
`credentials.json` (File contains OAuth2.0 Client ID and Client Secret)

## Installation

**INVOLVED APPS:**
- Python (3.11..)
- Tapo 

### 1. SHOULD HAVE A WINDOWS LAPTOP
> [!NOTE] 
> Tested using Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
> [!NOTE] 
> Always check "Use admin privilege..." and "Add python.exe to PATH" during installation to avoid errors
  	
- Download **[GAUTOCHARGER-V2](https://github.com/cleifwork/GAUTOCHARGER)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**
- Install EventGhost from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\EG_0.5.0-rc6_Setup'_ 
- Launch EventGhost
	- Click **'Open File'**
	- Load EventGhost Tree file from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\gautocharger_v2'_ 
	- Type **'shell:startup'** in the run window
	- Paste EventGhost shortcut in the startup window

### 2. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG _(Cuts/restores power supply to the laptop's power adapter)_
> Setting Up Your Tapo Smart Plug and Creating a Tapo Account

**Step 1: Unbox and Prepare Your Tapo Smart Plug**
- Unbox the Smart Plug:
	- _Remove the Tapo Smart Plug from its packaging._
	- _Ensure you have the plug and any included documentation._

- Choose a Location:
	- _Find a power outlet where you want to use the Tapo Smart Plug._
	- _Ensure the location has a stable Wi-Fi signal, as the plug will connect to your home network._

- Plug It In:
	- _Insert the Tapo Smart Plug into the chosen power outlet._
	- _The LED indicator on the plug should start blinking orange and green, indicating it’s ready to be set up._

**Step 2: Download and Install the Tapo App**
- Download the Tapo App:
	- _On your smartphone, open the App Store (iOS) or Google Play Store (Android)._
	- _Search for **"Tapo"** and download the official app developed by TP-Link._

- Install the App:
	- _Once downloaded, install the app on your smartphone._

**Step 3: Create a Tapo Account**
- Open the Tapo App:
	- _Launch the Tapo app on your smartphone._

- Sign Up for a Tapo Account:
	- _On the welcome screen, tap **"Sign Up."**_
	- _Enter your email address and create a password._
	- _Agree to the terms of service and privacy policy._
	- _Tap **"Sign Up."**_

- Verify Your Email Address:
	- _Check your email for a verification message from Tapo._
	- _Click the verification link in the email to confirm your account._

- Log In to Your Tapo Account:
	- _Return to the Tapo app and log in using your newly created account credentials._

**Step 4: Set Up the Tapo Smart Plug in the App**
- Add a New Device:
	- _After logging in, tap the "+" (plus) icon in the app to add a new device._
	- _Select **"Smart Plug"** from the list of devices._

- Connect to Wi-Fi:
	- _Follow the on-screen instructions to connect your smartphone to the Tapo Smart Plug's temporary Wi-Fi network (SSID)._
	- _Once connected, return to the Tapo app._

- Configure Wi-Fi Settings:
	- _The app will prompt you to select your home Wi-Fi network._
	- _Choose your Wi-Fi network, enter the password, and tap **"Next."**_
	- _The Tapo Smart Plug will connect to your home network._

- Name Your Smart Plug:
	- _Give your Smart Plug a name (e.g., **"GAUTOCHARGER"**)._
	- _Assign it to a room if you wish._

- Complete the Setup:
	- _Once the setup is complete, the LED indicator on the Smart Plug will turn solid green, indicating a successful connection._
	- _You can now control the plug via the Tapo app._

## Configuration
- **tapo_creds.txt**: Stores Tapo credentials (username, password) and IP address for the smart plug.
- **Battery Control Logic**: The script monitors battery levels every 20 seconds and performs charging control every 5 minutes. It turns on the smart plug when the battery falls below 20% and turns it off when the battery reaches 90%. These thresholds can be adjusted in the script.

## Logging
GAutoCharger-V2 logs battery levels and plug actions to a rotating log file located in the /logs/ directory. Logs are rotated daily, with each log file named script_log_YYYYMMDDHHMMSS.txt. Old logs are automatically cleaned up after 7 days.

## Retry Machanism
The script has a built-in retry mechanism for temporary connection issues with the Tapo Smart Plug. If the plug state fails to fetch or control actions are unsuccessful due to network issues, the script retries the action at the next check interval.

## How It Works
1. **Battery Monitoring**: The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **Smart Plug Control**: Based on the battery level thresholds, the script sends commands to the Tapo Smart Plug using the Tapo API to either turn on or off the charging.
3. **Logging**: Logs battery levels, plug states, and errors for debugging and tracking the system's behavior.

## Future Improvements
- Customizable battery thresholds via a configuration file.
- Integration with additional smart plug brands.
- More robust retry logic with exponential backoff for handling network failures.

## License
This project is licensed under the MIT License.

## Running Tests
- Add testing steps here...

## Optimizations
- Add optimization statements here...

## Screenshots
![App Screenshot](https://drive.google.com/uc?export=view&id=18M-28ac02I2GbAQpDuyhXgcNlsGsb8vU)

## Support

#### Join our FB Group
[GConnect App (Omada Voucher Solution)](https://www.facebook.com/groups/1776872022780742) 
  
#### Or subcribe to our YouTube Channel
[@JDIYMPH](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA)
## Tech Stack

**Client:** Python Script, Tapo

**Server:** TapoAPI
