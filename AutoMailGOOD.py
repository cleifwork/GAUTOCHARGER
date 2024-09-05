import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Function to log errors or messages to the script_log.txt
def log_to_file(log_file_path, message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{message}\n")

def read_desktop_path(log_file_path):
    try:
        # Use absolute path to source_path.txt using USERPROFILE
        user_profile = os.environ.get("USERPROFILE")
        source_path_file = os.path.join(user_profile, 'Desktop', 'GAUTOCHARGER', 'source_path.txt')

        # Read the desktop path from 'source_path.txt'
        with open(source_path_file, 'r') as f:
            desktop_path = f.read().strip()

        # Check if the path is valid
        if not desktop_path or not os.path.exists(desktop_path):
            raise FileNotFoundError("Desktop path not found or invalid.")

        return desktop_path
    except Exception as e:
        log_to_file(log_file_path, f"Error reading desktop path: {e}")
        raise

def send_email(subject, body, to_email):
    # Initialize log file path
    log_file_path = 'script_log.txt'

    try:
        # Read desktop path from source_path.txt
        desktop_path = read_desktop_path(log_file_path)

        # Define paths for credentials.json and token.json
        credentials_path = os.path.join(desktop_path, 'GAUTOCHARGER', 'credentials.json')
        token_path = os.path.join(desktop_path, 'GAUTOCHARGER', 'token.json')

        # Check if credentials.json exists
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"credentials.json not found at {credentials_path}")
        
        creds = None

        # Check if token.json exists
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # If no valid credentials, perform login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            # Build Gmail service
            service = build('gmail', 'v1', credentials=creds)

            # Create email message
            message = MIMEMultipart()
            message['to'] = to_email
            message['subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            message = {'raw': raw_message}

            # Send email
            send_message = service.users().messages().send(userId="me", body=message).execute()
            log_to_file(log_file_path, f'Message sent! Message Id: {send_message["id"]}')
        except HttpError as error:
            log_to_file(log_file_path, f'An error occurred during email send: {error}')

    except Exception as e:
        log_to_file(log_file_path, f"An error occurred: {e}")

# Usage
send_email("#PCBatteryGOOD", "", "trigger@applet.ifttt.com")
