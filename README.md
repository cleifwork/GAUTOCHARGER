# GAUTOCHARGER-V3 (SMTP): Laptop AutoCharging Solution
> [!NOTE] 
> _For Local Network & VPN Use_

**GAutoCharger-V3** is a battery management automation solution designed for laptops running Windows OS that function as servers and remain connected to a power source 24/7. This tool intelligently controls the charging process by managing a Tapo Smart Plug (e.g., P100) via Wi-Fi. It ensures that the battery is charged only when necessary, extending battery life and improving overall health by avoiding constant charging cycles.

### FEATURES
- Automated Charging Control: Automatically turns on the smart plug when the battery level is low and turns it off when the battery is full, based on configurable thresholds.
- Battery Level Monitoring: Logs battery levels and power status at regular intervals, providing full visibility into the device’s charging state.
- Smart Plug Integration: Communicates with Tapo Smart Plug through the Tapo API, allowing remote control of the power outlet connected to your laptop’s charger.
- Daily Log Rotation: Generates daily logs stored in the ```/logs/``` directory with automatic log rotation, ensuring minimal maintenance and easy tracking of battery status.
- Resilient Retry Mechanism: Built-in retry logic for handling temporary connection issues with the Tapo Smart Plug.
- Configurable Parameters: Easy-to-set thresholds and other parameters in the ```battery_level.config``` file for quick configuration.

### REQUIREMENTS
- **Python 3.11+** The script requires Python to execute the automation logic.
- **Python Libraries** (```psutil```)
- **IFTTT Account:** To receive email triggers and automate power control.
- **Tapo Account:** Required to manage your Tapo Smart Plugs.
- **Tapo Smart Plug:** Compatible models include P100, P105, etc.
- [**Google App Password**](https://myaccount.google.com/apppasswords) To allow email sending in python.


### DEMO
- [GAutoCharger-V3 App Demo](https://www.youtube.com/watch?v=QEfLKXhg03o)
- [GAutoCharger-V3 Installation & Configuration](https://www.youtube.com/watch?v=zHy7FS_HU7o)

### AUTHOR(S)
- [@cleifwork](https://www.github.com/cleifwork)

### ENVIRONMENT VARIABLES
To run this project, you will need to add your google app password in the `g_creds.config` file

### INSTALLATION

#### 1. SHOULD HAVE A WINDOWS LAPTOP
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

#### 2. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)** 

#### 3. SHOULD HAVE IFTTT ACCOUNT
- **[Signing Up for IFTTT Using Google Account on a Web Browser:](https://www.youtube.com/watch?v=dsIPK-fWXoc)**
	- _[IFTTT Website](https://ifttt.com/explore)_

- **Use these Published Applets:**
	- [PCBatteryLOW](https://ift.tt/XJS4DhE)
	- [PCBatteryGOOD](https://ift.tt/DkObnye)

> [!IMPORTANT]
> Add your **gmail** and **appass** in the ```g_creds.config``` file.

### CONFIGURATION
- **g_creds.config**: Stores the google app password for sending email.
- **Battery Control Logic**: The script monitors battery levels every 20 seconds and performs charging control every 1 minute. It turns on the smart plug when the battery falls below 20% and turns it off when the battery reaches 90%. These thresholds can be adjusted in the script.

### HOW IT WORKS
1. **Battery Monitoring**: The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **Smart Plug Control**: Based on the battery level thresholds, the script sends commands to the Tapo Smart Plug using the Tapo API to either turn ON or OFF the charging.
3. **Logging**: Logs battery levels

### FUTURE IMPROVEMENTS
- Add optimizations here...

### RUNNING TESTS
- Launch ```run_gautocharger.bat``` inside GAUTOCHARGER folder

### OPTIMIZATIONS
- Customizable battery thresholds and plug control frequency via a configuration file.

### SCREENSHOTS
![App Screenshot](https://drive.google.com/uc?export=view&id=1Vro6VWORnAFdjA1cgl-9VerqrLVbPYu7)

### SUPPORT
#### Join our [FB Group](https://www.facebook.com/groups/1776872022780742) Or subscribe to our [YouTube](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA) Channel

### TECH STACK
- **Client:** Python Script
- **Server:** IFTTT - Tapo Integration

