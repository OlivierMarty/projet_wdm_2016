import heapq

class Event():
    def __init__(self, date, location, description):
        self.date = date
        self.location = location
        self.description = description


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
