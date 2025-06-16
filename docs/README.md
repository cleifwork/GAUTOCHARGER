> [!IMPORTANT]
> **DON'T USE JUST YET ONGOING CONSTRUCTION !!!**

# GAUTOCHARGER-V4: Laptop AutoCharging Solution
> [!NOTE] 
> _For Local Network & VPN Use (Hybrid Version)_

**GAutoCharger-V4** is a battery management automation solution designed for laptops running Windows OS that function as servers and remain connected to a power source 24/7. This tool intelligently controls the charging process by managing a Tapo Smart Plug (e.g., P100) via Wi-Fi. It ensures that the battery is charged only when necessary, extending battery life and improving overall health by avoiding constant charging cycles.

## Features
- **Automated Charging Control:** Automatically turns on the smart plug when the battery level is low and turns it off when the battery is full, based on configurable thresholds.
- **Battery Level Monitoring:** Logs battery levels and power status at regular intervals, providing full visibility into the device’s charging state.
- **Daily Log Rotation:** Generates daily logs stored in the ```/logs/``` directory with automatic log rotation, ensuring minimal maintenance and easy tracking of battery status.
- **Configurable Parameters:** Easy-to-set thresholds and other parameters in the ```battery_level.config``` file for quick configuration.
- **Works with VPN:** Unlike V2 this version works even if you are connected to VPN.

## Requirements (OAuth2)
- **Python 3.11+:** Required to run the script.
- **Python Libraries:** (```psutil```)
- **IFTTT Account:** To receive email triggers and automate power control.
- **Tapo Account:** With IFTTT integration, required to manage your Tapo Smart Plugs.
- **Tapo Smart Plug:** Compatible models include P100, P105, etc.
- **Google OAuth 2.0:** To allow email sending in python in a more secure way.
- **Smartplug's IP must be STATIC** _(OPTIONAL FOR LOCAL NETWORK USE)_
- **Unofficial Tapo API: (for usage reference)** To work via local network

## Demo
- [GAutoCharger-V4 App Demo](https://www.youtube.com/watch?v=QEfLKXhg03o)
- [GAutoCharger-V4 Installation & Configuration](https://www.youtube.com/watch?v=zHy7FS_HU7o)

## Author
- [@cleifwork](https://www.github.com/cleifwork)

## Environment Variables
> [!NOTE]
> **FOR SMTP:** To run this project, you need to generate and add your [google app password](https://myaccount.google.com/apppasswords) in the `g_creds.config` file

> [!NOTE]
> **FOR OAuth2:** To run this project, you need to generate `credentials.json` from your [Google Cloud Console](https://console.cloud.google.com/)

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

- Download **[GAUTOCHARGER-V4](https://github.com/cleifwork/GAUTOCHARGER/tree/GAUTOCHARGER-V3)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**

### 2. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)** 

### 3. SHOULD HAVE IFTTT ACCOUNT
- **[Signing Up for IFTTT Using Google Account on a Web Browser:](https://www.youtube.com/watch?v=dsIPK-fWXoc)**
	- _[IFTTT Website](https://ifttt.com/explore)_

- **Use these Published Applets:**
	- [PCBatteryLOW](https://ift.tt/XJS4DhE)
	- [PCBatteryGOOD](https://ift.tt/DkObnye)

> [!IMPORTANT]
> **FOR LOCAL:** Add your **credentials.json** file in the GAUTOCHARGER root folder.

> [!IMPORTANT]
> **FOR OATH2:** Add your **credentials.json** file in the GAUTOCHARGER root folder.

## Configuration
- **g_creds.config:** Stores the google app password for sending email.
- **credentials.json** Generates token serves as credentials for sending email.
- **Battery Control Logic:** The script monitors battery levels every 20 seconds and performs charging control every 1 minute. It turns on the smart plug when the battery falls below 20% and turns it off when the battery reaches 90%. These thresholds can be adjusted in the script.

## How It Works?
#### FOR LOCAL
1. **Battery Monitoring:** The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **Google App Password:** Allows the python script to send SMTP email to IFTTT
3. **IFTTT-Tapo Integration:** Triggers the Tapo Smartplug (ON & OFF)
2. **Smart Plug Control:** Based on the battery level thresholds, the python script sends email to IFTTT to either turn ON or OFF the Tapo Smart Plug using their integration .
3. **Logging:** Logs battery levels

#### FOR OATH2
1. **Battery Monitoring:** The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **OAuth2.0 credentials.json:** Allows the python script to send a more secure email to IFTTT
3. **IFTTT-Tapo Integration:** Triggers the Tapo Smartplug (ON & OFF)
2. **Smart Plug Control:** Based on the battery level thresholds, the python script sends email to IFTTT to either turn ON or OFF the Tapo Smart Plug using their integration .
3. **Logging:** Logs battery levels


## Future Improvements
- Add future improvements here...

## Running Tests
- **FOR LOCAL:** Launch ```run_g2chargesmtp.bat``` inside GAUTOCHARGER folder
- **FOR OAuth2:** Launch ```run_g2chargeoauth.bat``` inside GAUTOCHARGER folder


## Optimizations
- PUT OPTIMIZATIONS HERE...

## Screenshots
![App Screenshot](https://drive.google.com/uc?export=view&id=1Vro6VWORnAFdjA1cgl-9VerqrLVbPYu7)

## Support
#### Join our [FB Group](https://www.facebook.com/groups/1776872022780742) Or subscribe to our [YouTube](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA) Channel

## Tech Stack
- **Client:** Python Script
- **Server:** IFTTT - Tapo Integration

