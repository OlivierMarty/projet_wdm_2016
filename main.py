import source
import config
from event import Event, HeapEvent
from datetime import datetime, timedelta
from time import sleep
import notification
from itertools import chain


def main():
    heap = HeapEvent()
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=10), "Villejuif", "descr Villejuif"))
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=3), "Cachan", "descr Cachan"))
    heap.push(Event(datetime.now()+timedelta(minutes=30, seconds=12), "université paris 7", "descr p7"))
    gap = timedelta(minutes=30) # 30 minutes : time to check trafic before an event
    while True:
        # TODO feed heap
        # then look for problems

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

if __name__ == "__main__":
    main()


#sources=chain(source.ratp_trafic(), source.transilien(), source.jcdecaux_vls())

#for source in sources:
#  if source.id in config.sources.get(source.source, []):
#    if source.problem():
#      notification.notify(source.message)
