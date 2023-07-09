import os
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from base64 import urlsafe_b64decode

def get_urls_from_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.modify'])
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Get unread emails
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    urls = []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()

        # Get the email body
        payload = msg['payload']
        parts = payload.get('parts')
        data = parts[0]['body']['data']
        body = urlsafe_b64decode(data).decode()

        # Extract URLs from the email body
        urls.extend(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body))
        # Mark the email as read
        service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

    return urls

