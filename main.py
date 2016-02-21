import source
import config
from event import Event, HeapEvent
from datetime import datetime, timedelta
from time import sleep
import notification
from analyse_event import *

def make_tz_aware(dt, tz='UTC', is_dst=None):
    """Add timezone information to a datetime object, only if it is naive."""
    tz = dt.tzinfo or tz
    try:
        tz = pytz.timezone(tz)
    except AttributeError:
        pass
    return tz.localize(dt, is_dst=is_dst) 



def main():
    heap = HeapEvent()
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=10), "Villejuif", "descr Villejuif"))
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=3), "Cachan", "descr Cachan"))
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=12), "université paris 7", "descr p7"))
    gap = timedelta(minutes=30) # 30 minutes : time to check trafic before an event
    
    list_event = get_events()
    for event in list_event:
        heap.push(event)
    
    while True:
        # TODO feed heap
      
        # sleep the min between 1 minute and the next event - gap
        next = timedelta(seconds=1) # TODO 1 minute
        if not heap.empty():
            next = min(next, heap.top().date-datetime.now()-gap)
        if next.total_seconds() > 0:
            print("Sleeping " + str(next))
            sleep(next.total_seconds())

        # next event
        if not heap.empty() and heap.top().date-datetime.now() < gap:
            event = heap.pop()
            print(event.description + " at " + event.location + ", " + str(event.date))

            # get useful ids of sources for this location
            ids_sources = source.from_location(event.location)
            # flatten this dictionnary
            ids_sources_flat = [item for (key, sublist) in ids_sources.items() for item in sublist]
            # grab info from internet for these sources
            sources=source.gen_sources(ids_sources)
            for src in sources:
              if src.id in ids_sources_flat and src.problem():
                # there is a problem ! We notify the user...
                notification.notify(src.message)

if __name__ == "__main__":
    main()
