# EasyGmailPython
A Python class for easily sending emails using the Gmail API with Oauth2.
modified from a tutorial found here https://www.thepythoncode.com/article/use-gmail-api-in-python
Will require a Google Workspace API environment to be set up
For info on how to set up, read https://developers.google.com/gmail/api/quickstart/python 
NOTE: you can stop before setting up quickstart.py as that functionality is integrated in this class
Ensure that when setting up your environment you enable full gmail scope or edit the scope in this class
as necessary.  
modified from a tutorial found here https://www.thepythoncode.com/article/use-gmail-api-in-python
Will require a Google Workspace API environment to be set up
For info on how to set up, read https://developers.google.com/gmail/api/quickstart/python 
NOTE: you can stop before setting up quickstart.py as that functionality is integrated in this class
Ensure that when setting up your environment you enable full gmail scope or edit the scope in this class as necessary.  

# Quickstart
- pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
- Create a new project in your Google Cloud Console dashboard
- Enable the Gmail API
- Configure your Oauth consent screen to include the Gmail API
- Create an OAuth 2.0 Clien ID of desktop type. Save the resulting file as credentials.json and add it to the same directory as gmail.py
- You will be prompted for authentication either by invoking Gmail._authenticate() or when initializing your first Gmail object.

# Usage
  from gmail import Gmail
## Create an email 
  email = Gmail('sender@email.com', 'receiver@email.com', 'title text', 'body text', 'signature')
  
  email = Gmail('sender@email.com', ['receiver1@email.com', 'receiver2@email.com'], 'title text', 'body text', 'signature')
  
  email = Gmail('sender@email.com', 'receiver@email.com', 'title text', 'body text', 'signature', ['attachment1.file', 'attachment2.file'])
  
  email = Gmail('sender@email.com', 'receiver@email.com', 'title text', 'body text', 'signature', ['attachment.file'], credential)
 
## Draft an email
  email.build()
  
  email.draft()
  
## Send an email
  email.build()
  
  email.send()
