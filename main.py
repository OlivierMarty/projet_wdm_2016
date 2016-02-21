from source import *
import config
from event import Event, HeapEvent
from datetime import datetime, timedelta
from time import sleep
import notification
from geocoding import position_of_location, k_neighbors
from gmail import get_list_event_gmail
from gcal import get_list_event_gcal

def make_tz_aware(dt, tz='UTC', is_dst=None):
    """Add timezone information to a datetime object, only if it is naive."""
    tz = dt.tzinfo or tz
    try:
        tz = pytz.timezone(tz)
    except AttributeError:
        pass
    return tz.localize(dt, is_dst=is_dst)

def gen_sources(sourceProviders, location):
  position = position_of_location(location)
  if not position:
    print("Unable to find a position for " + location)
  else:
    for sp in sourceProviders:
      # keep 2 nearest sources, if distance < 5 km
      ids = [id for (dist, id) in k_neighbors(sp.dic_of_positions(), position, 2) if dist < 5]
      print('Cherches les sources : ', ids)
      for source in sp.sources_of_ids(ids):
          yield source

def get_events():
    return get_list_event_gmail() + get_list_event_gcal()

def main():
    sourceProviders = [SourceProvider_ratp(),
      SourceProvider_jcdecaux_vls(),
      SourceProvider_transilien()]
    event_seen = set()
    heap = HeapEvent()
    manual = [Event('manual_1', datetime.now()+timedelta(minutes=30, seconds=10), "22 rue Henri Barbusse Villejuif", "descr Villejuif"),
      Event('manual_2', datetime.now()+timedelta(minutes=30, seconds=3), "68 rue Camille Desmoulins Cachan", "descr Cachan"),
      Event('manual_3', datetime.now()+timedelta(minutes=30, seconds=12), "université Paris Diderot", "descr p7")]
    gap = timedelta(minutes=30) # 30 minutes : time to check trafic before an event
    refresh = timedelta(seconds=30) # grab events every 30 secondes
    while True:
        # feed heap
        for event in get_events() + manual:
            # check if we already know it
            if event.id not in event_seen:
                event_seen.add(event.id)
                print()
                if (event.date - datetime.now()).total_seconds() < 0:
                    print("Ignore event in the past:")
                else:
                    print("Add event:")
                    heap.push(event)
                print(str(event))

        # sleep the min between 1 minute and the next event - gap
        next = refresh
        if not heap.empty():
            next = min(next, heap.top().date-datetime.now()-gap)
        if next.total_seconds() > 0:
            print()
            print("Sleeping " + str(next))
            sleep(next.total_seconds())

        # next event
        if not heap.empty() and heap.top().date-datetime.now() < gap:
            event = heap.pop()
            print()
            print("Check event:")
            print(str(event))

            # get useful ids of sources for this location, and grab info from internet
            sources=gen_sources(sourceProviders, event.location)
            if 'print' in config.notification['methods']:
                print() # show an empty line
            for src in sources:
              if src.problem():
                # there is a problem ! We notify the user...
                notification.notify(src.message)

if __name__ == "__main__":
    main()
