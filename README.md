
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
`g_creds.config` (file contains gmail credentials to authenticate gmail sending)

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
  	
- Download **[GAUTOCHARGER-V1](https://github.com/cleifwork/GAUTOCHARGER/tree/GAUTOCHARGER-V1)**
- Click Code > Download Zip
- Extract main folder to your Desktop
- Rename main folder to **'GAUTOCHARGER'**
- Install EventGhost from here ```'%USERPROFILE%\Desktop\GAUTOCHARGER\config\EG_0.5.0-rc6_Setup'```
- Launch EventGhost
	- Click **'Open File'**
	- Load EventGhost Tree file from here ```'%USERPROFILE%\Desktop\GAUTOCHARGER\config\gautocharger_v1'```
	- Type **'shell:startup'** in the run window
	- Paste EventGhost shortcut in the startup window

### 2. SHOULD HAVE A GOOGLE ACCOUNT
> [Obtain an App Password for Google Account](https://www.youtube.com/watch?v=MkLX85XU5rU)
1. **Enable 2-Step Verification:**
	- App passwords are only available if you have 2-Step Verification (also known as two-factor authentication) enabled on your Google account.
	- If you haven’t enabled it yet, follow these steps:
		1. Go to the Google Account Security page.
		2. Scroll down to “Signing in to Google” and click on 2-Step Verification.
		3. Click Get Started, follow the instructions, and set up 2-Step Verification (you can use your phone for this).
2. **Go to App Passwords:**
	- Once 2-Step Verification is enabled, go back to the Google Account Security page.
	- Scroll down to the “Signing in to Google” section.
	- Click on App passwords.
3. **Create an App Password:**
	- You may need to enter your Google account password again to access this page.
	- Under the Select app dropdown, choose Mail (or another option if you prefer).
	- Under Select device, choose the device you’ll be using the app password for (e.g., your computer).
	- Click Generate.
4. **Use the App Password:**
	- Google will generate a 16-character App Password. It will look something like this: abcd efgh ijkl mnop.
	- Copy the app password (without spaces) and use it in place of your Google account password in your script or app when sending emails.
5. **Save and Use the App Password:**
> [!NOTE] 
> The app password is displayed only once, so make sure you save it right away.
- Add and replace your gmail and app password in this file ```'%USERPROFILE%\Desktop\GAUTOCHARGER\g_creds.config'```


### 3. SHOULD HAVE TAPO ACCOUNT & SMARTPLUG (P100, P105)
> Creating a Tapo Account and Setting Up Your Tapo Smart Plug

- **[Create Tapo Account](https://www.youtube.com/watch?v=77Lt1sZykJg)**
- **[Setup Tapo Smart Plug](https://www.youtube.com/watch?v=Mbzdlxxn3cw)**

### 4. SHOULD HAVE IFTTT ACCOUNT
- **[Signing Up for IFTTT Using Google Account on a Web Browser:](https://www.youtube.com/watch?v=dsIPK-fWXoc)**
	- _Open your web browser and navigate to [IFTTT Website](https://ifttt.com/explore)_

- **Use these Published Applets:**
	- [PCBatteryLOW](https://ift.tt/XJS4DhE)
	- [PCBatteryGOOD](https://ift.tt/DkObnye)

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
