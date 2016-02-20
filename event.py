from gmail import *

class event:
    def __init__(self):
        pass

class Event(event):
    def __init__(self, date, location, subject, body, status, withwho, withwhomail):
        self.date = date
        self.location = location
        self.subject = subject
        self.body = body
        self.status = status
        self.withwho = withwho
        self.withwhomail = withwhomail
        
    def affiche(self):
        if self.status != "":
            print('<Status>: %s' % self.status)
        print('<Date>: %s' % self.date)
        if self.withwho != "" :
            print('<Organiser>: %s' % self.withwho)
        print('<Organiser\'s email>: %s' % self.withwhomail)
        
        if self.location != "":
            print('<Location>: %s' % self.location)
        print('<Subject>: %s' % self.subject)
        print('<Body>: %s' % self.body)
        
    def problem(self):
        #TODO: Call the function of RATP
        return "TODO"
    

