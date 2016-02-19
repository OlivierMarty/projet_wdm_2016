
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from gmail_msg import *
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart111'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def search(service, labels):
    while True:
        keyword = raw_input('Please enter a keyword to start searching the related messages in the mailbox(ctrl+c for quit) : ').lower()

        for i in range(3):
            print()
        
        #print('Labels:')
        for label in labels:
            if (label['name']=='INBOX'):
                print(label['name'])        
                list_msg = ListMessagesMatchingQuery(service,"me", query=keyword)
                #list_msg = ListMessagesWithLabels(service, "me", label['id'])
                #print(list_msg)
                i = 0
                for msg in list_msg:
                    i = i + 1
                    print()
                    print('Message #%d:'% i)
                    print('----')
                    msg = GetMessage(service,"me",msg['id'])
                    get_message_header(msg)
                    
                    mime_msg = GetMimeMessage(service,"me",msg['id'])
                    msg_body = get_message_body(mime_msg)
                    print('Body:')
                    print('%s' % msg_body)
                  
                    #print(GetMessage(service, "me", msg['id']))
                    #GetMimeMessage(service,"me",msg['id'])
        print()
        
def main():
    """
    Creates a Gmail API service object and outputs a list of messages which contain the keyword in the user's Gmail account.
   
    """
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        search(service, labels)

if __name__ == '__main__':
    main()

