#A class for sending and drafting using the Gmail API
#modified from a tutorial found here https://www.thepythoncode.com/article/use-gmail-api-in-python
#Will require a Google Workspace API environment to be set up
#For info on how to set up, read https://developers.google.com/gmail/api/quickstart/python 
#NOTE: you can stop before setting up quickstart.py as that functionality is integrated in this class
#Ensure that when setting up your environment you enable full gmail scope or edit the scope in this class
#as necessary.  
SCOPES = ['https://mail.google.com/']


import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
import base64
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

class Gmail:

    _email = None
    _draft = None

    def __init__(self, fro, to, title, body, signature, attachments = [], *creds):
        self.fro = fro
        if type(to) is list:
            self.to = ", ".join(to)
        else:
            self.to = to
        self.title = title
        self.body = body
        self.signature = signature
        self.attachments = attachments
        if creds:
            self.creds = creds
        else: 
            self.creds = self._authenticate()

    def __str__(self):
        return f"EMAIL\nFROM:{self.fro}\nTO:{self.to}\n{self.title}\n\n{self.body}\n{self.signature}\nATTACHMENTS:{self.attachments}\nUSING CREDENTIAL:{self.creds}"

    def build(self):
        if not self.attachments: # no attachments given
            self._email = MIMEText(self.body + '\n\n' + self.signature)
            self._draft = MIMEText(self.body + '\n\n' + self.signature)
            self._email['to'] = self._draft['to'] = self.to
            self._email['from'] = self._draft['from'] = self.fro
            self._email['subject'] = self._draft['subject'] = self.title
        else:
            self._email = MIMEMultipart()
            self._draft = MIMEMultipart()
            self._email['to'] = self._draft['to'] = self.to
            self._email['from'] = self._draft['from'] = self.fro
            self._email['subject'] = self._draft['subject'] = self.title
            self._email.attach(MIMEText(self.body + '\n\n' + self.signature))
            self._draft.attach(MIMEText(self.body + '\n\n' + self.signature))
            for filename in self.attachments:
                self.__add_attachment__(filename)

        self._email = {
            'raw': base64.urlsafe_b64encode(self._email.as_bytes()).decode()
        }
        self._draft = {
            'message': {
                'raw': base64.urlsafe_b64encode(self._draft.as_bytes()).decode()
                }
        }

    def __add_attachment__(self, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        self._email.attach(msg)
        self._draft.attach(msg)
    
    def send(self):
        return self.creds.users().messages().send(
            userId="me",
            body=self._email
        ).execute()

    def draft(self):
        return self.creds.users().drafts().create(
            userId="me",
            body=self._draft,
        ).execute()

    @staticmethod
    def _authenticate():
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)