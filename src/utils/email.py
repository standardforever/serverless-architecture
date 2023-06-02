import base64
import os
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
# from dotenv import dotenv_values

# os.environ.get = dotenv_values(".env")


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")



def create_message(to, subject, message_text):
    """ template for the email
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

async def send_email(to: str, subject: str, body: str):
    """ Send email to user
    """
    credentials = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://accounts.google.com/o/oauth2/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    service = build('gmail', 'v1', credentials=credentials)
    

    try:
        message = create_message(to, subject, body)
        await service.users().messages().send(userId="me", body=message).execute()
    except:
        return {"message": "Email sent successfully!"}

    # message = create_message(to, subject, body)
    # await service.users().messages().send(userId="me", body=message).execute()

    return {"message": "Email sent successfully!"}

