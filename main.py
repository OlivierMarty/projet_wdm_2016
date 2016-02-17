from class_xml import XML
import config
import notification
from itertools import chain
import datetime

class Event:
  def __init__(self):
    pass


class Event_ratp(Event):
  def __init__(self, ident, status, message):
    self.source = 'ratp_traffic'
    self.id = ident
    self.status = status
    self.message = message

  def problem(self):
    return self.status != 'normal'


def ratp_traffic():
  for tag in XML(url="http://www.ratp.fr/meteo/", lang="html").data.select('div.encadre_ligne'):
    yield Event_ratp(tag['id'], tag.img['alt'], tag.select('span.perturb_message')[0].string)


class Event_jcdecaux_vls_full(Event):
  def __init__(self, ident, nom, timestamp, places):
    self.source = 'jcdecaux_vls'
    self.id = ident + "_full"
    self.places = int(places)
    date = datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('à %Hh%M le %d/%m')
    self.message = 'Station vélo ' + nom.lower() + ' ' + date + ' : plus que ' + places + ' places disponibles !'

  def problem(self):
    return self.places <= 4 # TODO config


class Event_jcdecaux_vls_empty(Event):
  def __init__(self, ident, nom, timestamp, bikes):
    self.source = 'jcdecaux_vls'
    self.id = ident + "_empty"
    self.bikes = int(bikes)
    date = datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('à %Hh%M le %d/%m')
    self.message = 'Station vélo ' + nom.lower() + ' ' + date + ' : plus que ' + bikes + ' vélos !'

  def problem(self):
    return self.bikes <= 4 # TODO config


def jcdecaux_vls():
  ids = set(map(lambda s : s.split('_')[0], config.events['jcdecaux_vls']))
  for station in ids:
    xml = XML(url="https://api.jcdecaux.com/vls/v1/stations/" + station + "?contract=paris&apiKey="+config.api_key['jcdecaux'], lang="json")
    tag = xml.data.json
    yield Event_jcdecaux_vls_full(tag.number.string, tag.find('name').string, tag.last_update.string, tag.available_bike_stands.string)
    yield Event_jcdecaux_vls_empty(tag.number.string, tag.find('name').string, tag.last_update.string, tag.available_bikes.string)


events=chain(ratp_traffic(), jcdecaux_vls())

for event in events:
  if event.id in config.events.get(event.source, []):
    if event.problem():
      notification.notify(event.message)
