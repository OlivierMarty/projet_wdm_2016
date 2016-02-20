import source
import config
from event import Event, HeapEvent
import notification
from itertools import chain


def main():
    heap = HeapEvent()
    heap.push(Event(1, "Villejuif", "descr Villejuif"))
    heap.push(Event(0, "Cachan", "descr Cachan"))
    heap.push(Event(2, "université paris 7", "descr p7"))
    while True:
        # TODO feed heap
        # then sleep the min between 1 minutes and the next event (- 30 minutes ?)
        # then look for problems
        print(heap.top().location)
        print(heap.pop().location)

if __name__ == "__main__":
    main()


#sources=chain(source.ratp_trafic(), source.transilien(), source.jcdecaux_vls())

#for source in sources:
#  if source.id in config.sources.get(source.source, []):
#    if source.problem():
#      notification.notify(source.message)
