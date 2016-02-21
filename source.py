from class_xml import XML
import config
import datetime
from itertools import chain
import csv

# SOURCE CLASSES

class Source:
  pass

class SourceProvider:
  def dic_of_names(self):
    """Returns a dictionary mapping ids to name (for find.py)"""
    return []

  def dic_of_positions(self):
    """Returns a dictionary mapping ids to a list of positions (for geocoding.py)"""
    return []

  def sources_of_ids(self, ids):
    """Returns a generator of Source these ids"""
    return []


############## RATP ##############

class Source_ratp(Source):
  def __init__(self, ident, status, message):
    self.source = 'ratp_trafic'
    self.id = ident
    self.status = status
    self.message = message

  def problem(self):
    return self.status != 'normal'

class SourceProvider_ratp(SourceProvider):
  def __init__(self):
    self.names = None
    self.positions = None

  def dic_of_names(self):
    if not self.names:
      print('Téléchargement de la liste des lignes ratp...')
      xml = XML(url='http://www.ratp.fr/meteo/', lang='html')
      self.names = {tag['id']: tag['id'].replace('_', ' ') for tag in xml.data.select('.encadre_ligne')}
    return self.names

  def dic_of_positions(self):
    if not self.positions:
      self.positions = {}
      try:
        with open("ratp.csv", "r") as stations:
          for fields in csv.reader(stations, delimiter=',', quotechar='"'):
            lines = filter(lambda l: 'bus' not in l, fields[3].split(':')) # filter out bus line
            if lines:
              for line in lines:
                if line not in self.positions:
                  self.positions[line] = []
                self.positions[line].append((fields[1], fields[2]))
      except FileNotFoundError as e:
        print("[ERROR] ratp.csv not found\nDid you run 'python3 ratp_preprocessing.py > ratp.csv' ?")
        raise e
    return self.positions

  def sources_of_ids(self, ids):
    for tag in XML(url="http://www.ratp.fr/meteo/", lang="html").data.select('div.encadre_ligne'):
      if tag['id'] in ids:
        yield Source_ratp(tag['id'], tag.img['alt'],\
          tag['id'].replace('_', ' ') + ' : ' + tag.select('span.perturb_message')[0].string)


############## JCDECAUX_VLS ##############

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
    return super(Source_jcdecaux_vls_full, self).problem() or self.places <= config.sources_params['jcdecaux_vls']['limit_full']


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
    return super(Source_jcdecaux_vls_empty, self).problem() or self.bikes <= config.sources_params['jcdecaux_vls']['limit_empty']


class SourceProvider_jcdecaux_vls(SourceProvider):
  def __init__(self):
    self.names = {}
    self.positions = None

  def dic_of_names(self, contract=None):
    contract = contract or 'all'
    if contract not in self.names:
      print('Téléchargement de la liste des stations pour le contrat ' + contract + '...')
      if contract != 'all':
        xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?contract=' + contract + '&apiKey=' + config.api_key['jcdecaux_vls'], lang='json')
      else:
        xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?apiKey=' + config.api_key['jcdecaux_vls'], lang='json')
      self.names = {}
      for sta in xml.data.json.find_all("item", recursive=False):
        self.names[sta.contract_name.string.lower() + '_' + sta.number.string] =\
          sta.find('name').string + ' (' + sta.address.get_text() + ')'
        # we use find('name') because .name is the current tag name
    return self.names

  def dic_of_positions(self):
    if not self.positions:
      print('Téléchargement de la liste des stations...')
      xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?apiKey=' + config.api_key['jcdecaux_vls'], lang='json')
      self.positions = {}
      for sta in xml.data.json.find_all("item", recursive=False):
        self.positions[sta.contract_name.string.lower() + '_' + sta.number.string + '_' + 'full'] =\
          [(sta.lat.string, sta.lng.string)]
        # we use find('name') because .name is the current tag name
    return self.positions

  def sources_of_ids(self, ids):
    ids_set = set(map(lambda s : s.rsplit('_', 1)[0], ids))
    for station in ids_set:
      (contract, number) = list(station.split('_'))
      xml = XML(url="https://api.jcdecaux.com/vls/v1/stations/" + number + "?contract=" + contract + "&apiKey="+config.api_key['jcdecaux_vls'], lang="json")
      tag = xml.data.json
      if contract + '_' + number + '_full' in ids:
        yield Source_jcdecaux_vls_full(contract + '_' + number, tag.find('name').string, tag.last_update.string, tag.available_bike_stands.string, tag.status.string)
      if contract + '_' + number + '_empty' in ids:
        yield Source_jcdecaux_vls_empty(contract + '_' + number, tag.find('name').string, tag.last_update.string, tag.available_bikes.string, tag.status.string)


############## TRANSILIEN ##############

class Source_transilien(Source):
  def __init__(self, ident, message):
    self.source = 'transilien'
    self.id = ident
    self.message = message

  def problem(self):
    return self.message != 'Trafic normal'

class SourceProvider_transilien(SourceProvider):

  def __init__(self):
    self.names = None
    self.positions = None

  def dic_of_names(self):
    if not self.names:
      print('Téléchargement de la liste des lignes transilien...')
      xml = XML(url='http://www.transilien.com/info-trafic/temps-reel', lang='html')
      self.names = {}
      for line in xml.data.select('div.b_info_trafic')[0].find_all('div', recursive=False):
        id = line.select('.picto-transport')[1].get_text()
        self.names[id] = id.replace('-', ' ')
    return self.names

  def dic_of_positions(self):
    return {} # TODO

  def sources_of_ids(self, ids):
    xml = XML(url="http://www.transilien.com/info-trafic/temps-reel", lang="html").data
    container = xml.select('div.b_info_trafic')[0]
    for line in container.find_all('div', recursive=False):
      id = line.select('.picto-transport')[1].get_text()
      if id in ids:
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
