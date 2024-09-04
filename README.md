
> [!IMPORTANT]
> **DO NOT USE JUST YET - STILL UNDER DEVELOPMENT** 


# GAUTOCHARGER: AutoCharging Solution

**GAUTOCHARGER** is an automation solution designed for laptops running Windows OS that are used as servers and are connected to a charger 24/7. This solution helps manage the laptop's battery health by automatically disconnecting the power when charging is unnecessary. The process works by sending an email trigger to IFTTT from an EventGhost script, which then uses Tapo Smart Plugs (e.g., P100, P105, etc.) to control the power supply. This ensures that your server laptop remains charged without the risk of overcharging.

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
   
### 3. SHOULD HAVE IFTTT ACCOUNT _(Responds to the email trigger)_
- **Signing Up for IFTTT Using Google Account on a Web Browser:**
	- _Visit the [IFTTT Website](https://ifttt.com/explore)_
	- _Open your web browser and go to IFTTT's official website._

- **Start the Sign-Up Process:**
	- _Click on the **"Sign up"** button, usually located at the top right corner of the page._

- **Sign Up with Google:**
	- _Choose the **"Continue with Google"** option on the sign-up page._

- **Log in to Your Google Account:**
	- _A Google sign-in window will appear._
	- _Select the Google account you want to use._ 
	- _If you're not logged in, enter your Google email and password, then click "Next."_

- **Grant Permissions:**
	- _Review the permissions that IFTTT is requesting, then click **"Allow"** to grant access._

- **Complete the Sign-Up:**
	- _You’ll be redirected back to IFTTT. Follow any additional prompts to finalize your profile setup._
	- _Done! You're now signed up for IFTTT and can start creating applets._

### 4. SHOULD HAVE TAPO SMARTPLUG & TAPO ACCOUNT _(Cuts/restores power supply to the laptop's power adapter)_
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
