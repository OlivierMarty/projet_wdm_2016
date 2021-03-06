import heapq

class Event():
    """
      id : str
      date : type datetime.datetime
      location : str
      description : str
    """
    def __init__(self, id, date, location, description):
        self.id = id
        self.date = date
        self.location = location
        self.description = description

    def __str__(self):
        return """<Id>: """ + str(self.id) + """
<Date>: """ + str(self.date) + """
<Location>: """ + self.location + """
<Description>: """ + self.description


class HeapEvent():
    """Heap for event : sort event according to their dates"""
    def __init__(self):
        self.data = []

    def push(self, event):
        heapq.heappush(self.data, (event.date, event))

    def pop(self):
        return heapq.heappop(self.data)[1]

    def top(self):
        return self.data[0][1]

    def empty(self):
        return not self.data
