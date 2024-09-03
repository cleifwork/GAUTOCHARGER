
> [!IMPORTANT]
> **DO NOT USE JUST YET - STILL UNDER DEVELOPMENT** 


# GAUTOCHARGER: Automation Solution

**GAUTOCHARGER** is an automation solution designed for laptops running Windows OS that are used as servers and are connected to a charger 24/7. This solution helps manage the laptop's battery health by automatically disconnecting the power when charging is unnecessary. The process works by sending an email trigger to IFTTT from an EventGhost script, which then uses Tapo Smart Plugs (e.g., P100, P103, etc.) to control the power supply. This ensures that your server laptop remains charged without the risk of overcharging.

## **Requirements**
- **EventGhost:** To run the automation script.
- **IFTTT Account:** To receive email triggers and automate power control.
- **Tapo Smart Plug:** Compatible models include P100, P103, etc.
- **Tapo Account:** Required to manage your Tapo Smart Plugs.
- **Python 3.11:** The script requires Python to execute the automation logic.

## **How It Works**
- **Trigger:** EventGhost monitors the laptop's battery level and executes a script that sends an email to IFTTT when the battery level reaches a predefined threshold.
- **Action:** IFTTT then controls the Tapo Smart Plug to either cut or restore power to your laptop's charger.
- **Result:** Your laptop stays optimally charged without being constantly connected to power.

## Demo

-   [GConnect App Demo](https://www.youtube.com/)
-   [GConnect Installation & Configuration](https://www.youtube.com/)


## Authors

- [@cleifwork](https://www.github.com/cleifwork)
## Environment Variables

To run this project, you will need to add the following environment variables to your **GAUTOCHARGER** folder.
`credentials.json` (File contains OAuth2.0 Client ID and Client Secret)

## Installation & Configuration

**INVOLVED APPS:**
- EventGhost (included)
- Python (3.11..)
- Google 
- IFTTT 
- Tapo 


### REQUIREMENTS:

**1. SHOULD HAVE A WINDOWS LAPTOP** 
> [!NOTE] 
> Tested using Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
> [!NOTE] 
> Always check "Use admin privilege..." and "Add python.exe to PATH" during installation to avoid errors
  	
- Download **[GAUTOCHARGER](https://github.com/cleifwork/GAUTOCHARGER)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**
- Install EvenGhost from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\EG_0.5.0-rc6_Setup'_ 
- Launch EventGhost
	- Click **'Open File'**
	- Load EventGhost Tree file from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\gautocharger_v2'_ 
	- Type **'shell:startup'** in the run window
	- Paste EventGhost shortcut in the startup window

**2. SHOULD HAVE A GOOGLE ACCOUNT**
-   Login to to your google account
-   Goto [Google Cloud Console](https://console.cloud.google.com/)
-   Create a **NEW PROJECT** 
> [!TIP]
> You may use existing project or create a new project
-   Goto **APIs & Services**
    -   Click _"Credentials"_ (with the key icon)
    -   Click **'+CREATE CREDENTIALS'**
	-   Select **'OAuth client ID'**
    -   Select **'Application type'** in the dropdown list: **'Desktop app'**
	-   Give it a Name _(OPTIONAL)_
	-   Click **'CREATE'**
	-   Click **'DOWNLOAD JSON'**
	-   Rename file to _"credentials"_ before saving to _**'%USERPROFILE%\Desktop\GAUTOCHARGER'**_  
   
**3. SHOULD HAVE IFTTT ACCOUNT** (Responds to the email trigger)
> [!IMPORTANT]
> SOME REQUIREMENTS: 

**4. SHOULD HAVE TAPO SMARTPLUG** (Cuts/restores power supply to the laptop's power adapter)
> [!IMPORTANT]
> SOME REQUIREMENTS: 

**5. SHOULD HAVE TAPO ACCOUNT** (Manages the Tapo SmartPlug)
> [!IMPORTANT]
> SOME REQUIREMENTS: 

## Running Tests
-   Add testing steps here...

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

**Client:** EventGhost/Python Script, Tapo

**Server:** Google OAuth 2.0 Server, Gmail, IFTTT 
