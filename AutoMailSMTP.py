import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to log errors or messages to the script_log.txt
def log_to_file(log_file_path, message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{message}\n")
        
# Function to read Gmail credentials from g_creds.config
def read_gmail_credentials(config_path):
    credentials = {}
    try:
        with open(config_path, 'r') as config_file:
            for line in config_file:
                key, value = line.strip().split('=')
                credentials[key] = value
        return credentials['gmail'], credentials['appass']
    except Exception as e:
        raise Exception(f"Error reading credentials: {e}")

def send_email(subject, body, to_email):
    # Initialize log file path
    log_file_path = 'script_log.txt'

    try:
        # Read log file path from current working directory
        current_path = os.getcwd()  # Get the current working directory
        log_path = os.path.join(current_path, log_file_path) 

        # Path to g_creds.config on the desktop
        config_path = os.path.join(current_path, 'g_creds.config')

        # Read Gmail credentials from config file
        gmail_user, app_password = read_gmail_credentials(config_path)

        # Gmail SMTP configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # TLS port

        # Create the email message
        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()  # Identify ourselves to the SMTP server
            server.starttls()  # Secure the connection
            server.ehlo()  # Re-identify ourselves as an encrypted connection
            server.login(gmail_user, app_password)  # Login with the app password

            # Send the email
            server.sendmail(gmail_user, to_email, message.as_string())
            server.quit()  # Close the SMTP server connection

            log_to_file(log_file_path, f'Email sent successfully to {to_email}')
        except Exception as e:
            log_to_file(log_file_path, f'Error sending email: {e}')

    except Exception as e:
        log_to_file(log_file_path, f"An error occurred: {e}")
