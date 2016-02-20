from gmail import *
from gcal import *

def main():

    mc = input('Please enter m(for gmail) or c (for google calendar) to start the events finder: ').lower()
    if (mc == 'm'):
        list_event = get_list_event_gmail()
    else:
        list_event = get_list_event_gcal()
  
    for event in list_event:
        event.affiche()
    
if __name__ == '__main__':
    main()
