from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from event import *

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python'


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
                                   'calendar-python-quickstart.json')

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



def find_list_event_gcal(events):
    list_event = []
    
    if not events:
        print('No upcoming events found.')
        return list_event

    i = 0

    for event in events:
        i = i + 1
        #print('The event #', i,'------------------------')
        start = event['start'].get('dateTime', event['start'].get('date'))

        #status :  confirmed or not
        status = event['status']
        #print('  Status:', event['status'])     
        
        #htmlLink:  the url of the event
        #print('  HtmlLink:', event['htmlLink'])
        
        #created:   the created time of the event
        #print('  Created time:', event['created'])
        
        #updateed:   the updated time of the event
        #print('  Updatedtime:', event['updated'])
        
        body = ""
        if ('description' in event):
            body = event['description']
            #print('  Description:', event['description'])
       
        subject = ""
        if ('summary' in event):
            subject = event['summary']
            #print('  Sumarry:', event['summary'])
        
        location = ""
        if ('location' in event):
            location = event['location']
            if (type(location) == 'bytes'):
                location = location.decode()
            #print('  Location:', event['location'])

        #print("  Organizer's name:", event['organizer'].get('displayName', 'unknown'))
        withwho =  event['organizer'].get('displayName', 'unknown')

        #print("  Organizer's email:", event['organizer']['email'])
        withwhomail =  event['organizer']['email']

        #print("  Start time:", event['start']['dateTime'])
        #print(start, event['summary']);


        list_event.append(Event(start,location,body,"c"))
        return list_event
 
def get_list_event_gcal():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events...')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    return find_list_event_gcal(events)

