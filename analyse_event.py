from gmail import *
from gcal import *

def get_events():
    return get_list_event_gmail() + get_list_event_gcal()

def main():
    for event in get_events():
        event.affiche()

if __name__ == '__main__':
    main()
