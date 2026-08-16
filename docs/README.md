# GAUTOCHARGER-V4: Laptop AutoCharging Solution
> [!NOTE] 
> _For local-network control with a Home Assistant email fallback._

**GAutoCharger-V4** is a battery management automation solution designed for laptops running Windows OS that function as servers and remain connected to a power source 24/7. This tool intelligently controls the charging process by managing a Tapo Smart Plug (e.g., P100) via Wi-Fi. It ensures that the battery is charged only when necessary, extending battery life and improving overall health by avoiding constant charging cycles.

## Features
- **Automated Charging Control:** Automatically turns on the smart plug when the battery level is low and turns it off when the battery is full, based on configurable thresholds.
- **Battery Level Monitoring:** Logs battery levels and power status at regular intervals, providing full visibility into the device’s charging state.
- **Daily Log Rotation:** Generates daily logs stored in the ```/logs/``` directory with automatic log rotation, ensuring minimal maintenance and easy tracking of battery status.
- **Configurable Parameters:** Easy-to-set thresholds and other parameters in the ```battery_level.config``` file for quick configuration.
- **VPN-safe fallback:** When local Tapo control is unavailable (for example, while a VPN blocks LAN traffic), the script sends a Gmail command email to Home Assistant.

## Requirements
- **Home Assistant:** An always-on Home Assistant instance on the same home network as the Tapo plug, with the TP-Link Smart Home integration configured.
- **Gmail account:** A Gmail account authorized through the Gmail API with the `gmail.send` OAuth scope.
- **Home Assistant IMAP integration:** Configured to watch the command inbox and run separate ON and OFF email automations.
- **Tapo Smart Plug:** Compatible models include P100, P105, etc.
- **Smartplug's IP must be STATIC** _(OPTIONAL FOR LOCAL NETWORK USE)_
- **Unofficial Tapo API: (for usage reference)** To work via local network

## Demo
- [GAutoCharger-V4 App Demo](https://www.youtube.com/watch?v=QEfLKXhg03o)
- [GAutoCharger-V4 Installation & Configuration](https://www.youtube.com/watch?v=zHy7FS_HU7o)

## Author
- [@cleifwork](https://www.github.com/cleifwork)

## Private configuration
> [!NOTE]
> **FOR LOCAL:** To run this project, you need to add your tapo credentials and static IP in this file `tapo_creds.config`.

> [!NOTE]
> **FOR HOME ASSISTANT EMAIL:** Copy `app/home_assistant_email.config.example` to `app/home_assistant_email.config`. Add the Home Assistant command inbox and the exact ON/OFF email subjects used by your Home Assistant automations. This file is ignored by Git. The sender is the Gmail account previously authorized through `credentials.json` and `token.json`.

## Installation
### 1. SHOULD HAVE A WINDOWS LAPTOP
> [!NOTE] 
> Tested using Windows 10 and Windows 11
- Download **[GAUTOCHARGER-V4](https://github.com/cleifwork/GAUTOCHARGER/tree/GAUTOCHARGER-V4)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**

### 2. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)** 

### 3. Configure the Home Assistant email fallback
1. In Home Assistant, use the IMAP integration to monitor your command Gmail inbox.
2. Create one `imap_content` event automation to turn the plug on and another to turn it off. Filter each automation by the sender and its unique command subject.
3. Copy `app/home_assistant_email.config.example` to `app/home_assistant_email.config`.
4. Set `to_email` to the inbox monitored by Home Assistant. The sender is the Gmail account authorized through `credentials.json` and `token.json`.
5. Set `on_subject` and `off_subject` to exactly match the corresponding Home Assistant automation filters.

## Configuration
- **tapo_creds.config:** Stores your tapo credentials.
- **home_assistant_email.config:** Stores the Home Assistant command inbox and private ON/OFF email command subjects.
- **Battery Control Logic:** The script checks at the configured interval, turns the plug on at the ON threshold, and turns it off at the OFF threshold. It uses local Tapo control first, then sends the Home Assistant email command only if local control fails.

## How It Works?
#### Local Tapo control
1. **Battery Monitoring:** The script uses the psutil library to monitor the laptop's battery percentage and charging status.
2. **Smart Plug Control:** The script attempts to call the Tapo plug at its local IP address.
3. **Logging:** Logs battery levels and control results.

#### Home Assistant email fallback
1. If local Tapo control fails, the script sends the command through the Gmail API using the least-privilege `gmail.send` OAuth scope.
2. It sends either the configured ON or OFF command subject to the Home Assistant command inbox.
3. Home Assistant receives the email through IMAP and its matching automation controls the local Tapo plug.


## Future Improvements
- Add future improvements here...

## Running Tests
- Launch ```launchpad.bat``` inside GAUTOCHARGER folder

## Optimizations
- Made the app portable, no python libs needed, run anywhere

## Screenshots
![App Screenshot](https://drive.google.com/uc?export=view&id=1Vro6VWORnAFdjA1cgl-9VerqrLVbPYu7)

## Support
#### Join our [FB Group](https://www.facebook.com/groups/1776872022780742) Or subscribe to our [YouTube](https://www.youtube.com/channel/UC9O3ezuyjS7C6V7-ZAHCQrA) Channel

## Tech Stack
- **Client:** Python Script, psutil
- **Server:** Home Assistant, Gmail API/IMAP, TP-Link Smart Home integration, Unofficial Tapo API

