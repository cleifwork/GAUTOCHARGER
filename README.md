
> [!IMPORTANT]
> **DO NOT USE JUST YET - STILL UNDER DEVELOPMENT** 


# GAUTOCHARGER (SMTP): AutoCharging Solution

**GAUTOCHARGER** is an automation solution designed for laptops running Windows OS that are used as servers and are connected to a charger 24/7. This solution helps manage the laptop's battery health by automatically disconnecting the power when charging is unnecessary. The process works by sending an email trigger to IFTTT from an EventGhost script, which then uses Tapo Smart Plugs (e.g., P100, P105, etc.) to control the power supply. This ensures that your server laptop remains charged without the risk of overcharging.

## **Requirements**
- **EventGhost:** To trigger the automation script. Runs in the background.
- **IFTTT Account:** To receive email triggers and automate power control.
- **Tapo Smart Plug:** Compatible models include P100, P105, etc.
- **Tapo Account:** Required to manage your Tapo Smart Plugs.
- **Python 3.11+** The script requires Python to execute the automation logic.

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


## REQUIREMENTS:

### 1. SHOULD HAVE A WINDOWS LAPTOP
> [!NOTE] 
> Tested using Windows 10 and Windows 11

- [Install python](https://www.python.org/downloads/) (recommended version: _**python-3.11.4**_)
> [!NOTE] 
> Always check "Use admin privilege..." and "Add python.exe to PATH" during installation to avoid errors
  	
- Download **[GAUTOCHARGER](https://github.com/cleifwork/GAUTOCHARGER)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**
- Install EventGhost from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\EG_0.5.0-rc6_Setup'_ 
- Launch EventGhost
	- Click **'Open File'**
	- Load EventGhost Tree file from here _'%USERPROFILE%\Desktop\GAUTOCHARGER\config\gautocharger_v2'_ 
	- Type **'shell:startup'** in the run window
	- Paste EventGhost shortcut in the startup window

### 2. SHOULD HAVE A GOOGLE ACCOUNT
   
### 3. SHOULD HAVE IFTTT ACCOUNT
- **Signing Up for IFTTT Using Google Account on a Web Browser:**
	- _Open your web browser and navigate to [IFTTT Website](https://ifttt.com/explore)_

- **Start the Sign-Up Process:**
	- _Click on the **"Sign up"** button, usually located at the top right corner of the page._

- **Sign Up with Google:**
	- _On the sign-up page, select the **"Continue with Google"** option._

- **Log in to Your Google Account:**
	- _A Google sign-in window will pop up._
	- _Select the Google account you want to use for IFTTT._ 
	- _If you're not logged in, enter your Google email and password, then click "Next."_

- **Grant Permissions:**
	- _Review the permissions that IFTTT is requesting, then click **"Allow"** to grant access._

- **Complete the Sign-Up:**
	- _You’ll be redirected back to IFTTT. Follow any additional prompts to finalize your profile setup._
	- _Done! You're now signed up for IFTTT and can start creating applets._

- **Use these Published Applets:**
	- [PCBatteryLOW](https://ift.tt/XJS4DhE)
	- [PCBatteryGOOD](https://ift.tt/DkObnye)

### 4. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)**


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

**Server:** GMail (SMTP), IFTTT 
