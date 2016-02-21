from gmail import *
from gcal import *

def get_events():
    return get_list_event_gcal()

    #return get_list_event_gmail() + get_list_event_gcal()

def main():
    for event in get_events():
        print(str(event))

if __name__ == '__main__':
    main()
