# GAUTOCHARGER-V3 (SMTP): AutoCharging Solution - FOR VPN USE

**GAutoCharger-V3** is a battery management automation solution designed for laptops running Windows OS that function as servers and remain connected to a power source 24/7. This tool intelligently controls the charging process by managing a Tapo Smart Plug (e.g., P100) via Wi-Fi. It ensures that the battery is charged only when necessary, extending battery life and improving overall health by avoiding constant charging cycles.

## Features
- Automated Charging Control: Automatically turns on the smart plug when the battery level is low and turns it off when the battery is full, based on configurable thresholds.
- Battery Level Monitoring: Logs battery levels and power status at regular intervals, providing full visibility into the device’s charging state.
- Smart Plug Integration: Communicates with Tapo Smart Plug through the Tapo API, allowing remote control of the power outlet connected to your laptop’s charger.
- Daily Log Rotation: Generates daily logs stored in the ```/logs/``` directory with automatic log rotation, ensuring minimal maintenance and easy tracking of battery status.
- Resilient Retry Mechanism: Built-in retry logic for handling temporary connection issues with the Tapo Smart Plug.
- Configurable Parameters: Easy-to-set thresholds and other parameters in the ```battery_level.config``` file for quick configuration.

## Requirements
- **Python 3.11+** The script requires Python to execute the automation logic.
- **Python Libraries** (```psutil```)
- **IFTTT Account:** To receive email triggers and automate power control.
- **Tapo Account:** Required to manage your Tapo Smart Plugs.
- **Tapo Smart Plug:** Compatible models include P100, P105, etc.
- **Google App Password** [Need to generate app password to allow email sending](https://myaccount.google.com/apppasswords) 


## Demo
- [GAutoCharger-V3 App Demo](https://www.youtube.com/watch?v=QEfLKXhg03o)
- [GAutoCharger-V3 Installation & Configuration](https://www.youtube.com/watch?v=zHy7FS_HU7o)

## Authors
- [@cleifwork](https://www.github.com/cleifwork)

## Environment Variables
To run this project, you will need to add the following environment variables to your **GAUTOCHARGER** folder.
`tapo_creds.config`

## Installation

### 1. SHOULD HAVE A WINDOWS LAPTOP
> [!NOTE] 
> Tested using Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
> [!NOTE] 
> Always check "Use admin privilege..." and "Add python.exe to PATH" during installation to avoid errors

**Install the following libraries via CMD**
```
pip install tapo psutil
```

- Download **[GAUTOCHARGER-V3](https://github.com/cleifwork/GAUTOCHARGER/tree/GAUTOCHARGER-V3)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**

### 2. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)** 
- **[How to get Tapo Smart Plug's IP & MAC address then set to STATIC in your router](https://www.youtube.com/watch?v=lYJgfnz1bg0)**

> [!IMPORTANT]
> Replace **username**, **password** and **ip_address** in the ```tapo_creds.config``` file with your tapo account and smartplug's IP

## Configuration
- **g_creds.config**: Stores the google app password for sending email.
- **Battery Control Logic**: The script monitors battery levels every 20 seconds and performs charging control every 1 minute. It turns on the smart plug when the battery falls below 20% and turns it off when the battery reaches 90%. These thresholds can be adjusted in the script.

## How It Works
1. **Battery Monitoring**: The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **Smart Plug Control**: Based on the battery level thresholds, the script sends commands to the Tapo Smart Plug using the Tapo API to either turn ON or OFF the charging.
3. **Logging**: Logs battery levels

## Future Improvements
- More robust retry logic with exponential backoff for handling network failures.

## Running Tests
- (CMD) Ping smartplug's IP from the laptop to confirm they're on the same network
    - IF NOT need to troubleshoot
    - IF OK proceed to the **NEXT STEP**
- **NEXT STEP:** Launch ```run_gautocharger.bat``` inside GAUTOCHARGER folder

## Optimizations
- Customizable battery thresholds and plug control frequency via a configuration file.

## Screenshots
![App Screenshot](https://drive.google.com/uc?export=view&id=1Vro6VWORnAFdjA1cgl-9VerqrLVbPYu7)

## Support

#### Join our FB Group
[GConnect App (Omada Voucher Solution)](https://www.facebook.com/groups/1776872022780742) 
  
#### Or subcribe to our YouTube Channel
[@JDIYMPH](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA)

## Tech Stack
- **Client:** Python Script
- **Server:** IFTTT - Tapo Integration

