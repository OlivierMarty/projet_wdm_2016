import heapq

class Event():
    def __init__(self, date, location, description, eid = "c"):
        self.date = date
        self.location = location
        self.description = description
        self.eid = eid

    def affiche(self):
        print('<Date>: %s' % self.date)
        print('<Location>: %s' % self.location)

        if (self.eid == "m"):
            print('<Description>: %s' % self.description.decode())
        elif (self.eid == "c"):
            print('<Body>: %s' % self.description)       
              
    def problem(self):
        #TODO: Call the function of RATP
        return "TODO"

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

        
 
    

