
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from gmail_msg import *
from event import *
from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/projet-wdm-gmail.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python'


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
    credential_path = os.path.join(credential_dir, 'projet-wdm-gmail.json')

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

def get_list_event_gmail():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    print('Getting mails matching "Rendez-vous" from Gmail...')


    list_event = []
    if not labels:
        print('No labels found.')
        return list_event

    for label in labels:
        if (label['name']=='INBOX'):
            list_msg = ListMessagesMatchingQuery(service,"me", query="Rendez-vous")
            for msg in list_msg:
                msg = GetMessage(service,"me",msg['id'])
                mime_msg = GetMimeMessage(service,"me",msg['id'])
                body = get_message_body(mime_msg)
                try:
                    # Parse only messages in the format + not lenient (do not check keywords etc)
                    # Rendez-vous
                    # le 22/02/2016 11h00
                    # à l'université Paris Diderot
                    # pour le cours de WDM
                    lines = body.replace('\r', '').split('\n')
                    if len(lines) >= 4 and lines[0] == 'Rendez-vous':
                        date = datetime.strptime(lines[1][3:], '%d/%m/%Y %Hh%M')
                        location = lines[2][2:]
                        description = lines[3]
                        list_event.append(Event('gmail_'+msg['id'], date,location,description))
                except Exception as e:
                    raise e
    return list_event
