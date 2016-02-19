from class_xml import XML
import config
import datetime

# SOURCE CLASSES

class Source:
  def __init__(self):
    pass


class Source_ratp(Source):
  def __init__(self, ident, status, message):
    self.source = 'ratp_trafic'
    self.id = ident
    self.status = status
    self.message = message

  def problem(self):
    return self.status != 'normal'

class Source_jcdecaux_vls(Source):
  def __init__(self, ident, nom, timestamp, status):
    self.source = 'jcdecaux_vls'
    self.id = ident
    self.status = status # TODO dans l'API pour 1 station il semble que c'est toujours OPEN :-(
    self.date = datetime.datetime.fromtimestamp(int(timestamp)/1000).strftime('à %Hh%M le %d/%m')
    if status != "OPEN":
      self.message = 'Station vélo ' + nom.lower() + ' ' + self.date + ' : fermée !'
    else:
      self.message = None

  def problem(self):
    return self.status != "OPEN"

class Source_jcdecaux_vls_full(Source_jcdecaux_vls):
  def __init__(self, ident, nom, timestamp, places, status):
    super(Source_jcdecaux_vls_full, self).__init__(ident, nom, timestamp, status)
    self.id += "_full"
    self.places = int(places)
    if not self.message:
      self.message = 'Station vélo ' + nom.lower() + ' ' + self.date + ' : '
      if self.places == 0:
        self.message += 'plus de place !'
      elif self.places == 1:
        self.message += 'plus qu\'une place !'
      else:
        self.message += 'plus que ' + places + ' places disponibles !'

  def problem(self):
    return super(Source_jcdecaux_vls_full, self).problem() or self.places <= 4 # TODO config


class Source_jcdecaux_vls_empty(Source_jcdecaux_vls):
  def __init__(self, ident, nom, timestamp, bikes, status):
    super(Source_jcdecaux_vls_empty, self).__init__(ident, nom, timestamp, status)
    self.id += "_empty"
    self.bikes = int(bikes)
    if not self.message:
      self.message = 'Station vélo ' + nom.lower() + ' ' + self.date + ' : '
      if self.bikes == 0:
        self.message += 'plus de vélo !'
      elif self.bikes == 1:
        self.message += 'plus qu\'un vélo !'
      else:
        self.message += 'plus que ' + bikes + ' vélos !'

  def problem(self):
    return super(Source_jcdecaux_vls_empty, self).problem() or self.bikes <= 4 # TODO config


class Source_transilien(Source):
  def __init__(self, ident, message):
    self.source = 'transilien'
    self.id = ident
    self.message = message

  def problem(self):
    return self.message != 'Trafic normal'


# SOURCES GENERATORS

def ratp_trafic():
  for tag in XML(url="http://www.ratp.fr/meteo/", lang="html").data.select('div.encadre_ligne'):
    yield Source_ratp(tag['id'], tag.img['alt'], tag.select('span.perturb_message')[0].string)


def jcdecaux_vls():
  ids = set(map(lambda s : s.rsplit('_', 1)[0], config.sources['jcdecaux_vls']))
  for station in ids:
    (contract, number) = list(station.split('_'))
    xml = XML(url="https://api.jcdecaux.com/vls/v1/stations/" + number + "?contract=" + contract + "&apiKey="+config.api_key['jcdecaux'], lang="json")
    tag = xml.data.json
    yield Source_jcdecaux_vls_full(contract + '_' + number, tag.find('name').string, tag.last_update.string, tag.available_bike_stands.string, tag.status.string)
    yield Source_jcdecaux_vls_empty(contract + '_' + number, tag.find('name').string, tag.last_update.string, tag.available_bikes.string, tag.status.string)


def transilien():
  xml = XML(url="http://www.transilien.com/info-trafic/temps-reel", lang="html").data
  container = xml.select('div.b_info_trafic')[0]
  for line in container.find_all('div', recursive=False):
    id = line.select('.picto-transport')[1].get_text()
    message = ""
    for c in line.select_one('.title').children:
      if c.name: # a tag
        if 'picto-transport' not in c.attrs.get('class', ''):
          message += c.get_text()
      else: # a string
        message += c
    for det in line.select('.item-disruption'):
      message += det.get_text()
    message = " ".join(message.split()) # delete multiple spaces
    yield Source_transilien(id, message)
