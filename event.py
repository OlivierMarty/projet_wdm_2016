from gmail import *

class event:
    def __init__(self):
        pass

class Event(event):
    def __init__(self, date, location, body, eid):
        self.date = date
        self.location = location
        self.body = body
        self.eid = eid
        
    def affiche(self):
        print('<Date>: %s' % self.date)
        print('<Location>: %s' % self.location)

        if (self.eid == "m"):
            print('<Body>: %s' % self.body.decode())
        elif (self.eid == "c"):
            print('<Body>: %s' % self.body)       
              
    def problem(self):
        #TODO: Call the function of RATP
        return "TODO"
    

