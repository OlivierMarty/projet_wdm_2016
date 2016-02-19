import config
from class_xml import XML


def find_id():
  t = int(input('Sélectionnez la source :\n\t1 : ratp\n\t2 : transilien\n\t3 : jcdecaux_vls (vélos en libre service)\n'))
  if t == 1: # RATP
    print('Téléchargement de la liste des lignes...')
    xml = XML(url='http://www.ratp.fr/meteo/', lang='html')
    dic = {tag['id']: tag['id'].replace('_', ' ') for tag in xml.data.select('.encadre_ligne')}

  elif t == 2: # transilien
    print('Téléchargement de la liste des lignes...')
    xml = XML(url='http://www.transilien.com/info-trafic/temps-reel', lang='html')
    dic = {}
    for line in xml.data.select('div.b_info_trafic')[0].find_all('div', recursive=False):
      id = line.select('.picto-transport')[1].get_text()
      dic[id] = id.replace('-', ' ')

  elif t == 3: # jcdecaux_vls
    print('Téléchargment de la liste des villes...')
    xml_contracts = XML(url='https://api.jcdecaux.com/vls/v1/contracts?apiKey=' + config.api_key['jcdecaux'], lang='json')
    contracts = {tag.find('name').string : tag.commercial_name.string for tag in xml_contracts.data.json.children}
    while True:
      print('Choisissez une ville :')
      for (name, commercial_name) in contracts.items():
        print(name + ' (' + commercial_name + ')')
      print("toutes (toutes les villes)\n")
      contract = input()
      if contract == 'toutes':
        contract = None
        break;
      if contract in contracts:
        break;
      print("Ville inconnue !\n\n")
    print('Téléchargement de la liste des stations...')
    if contract:
      xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?contract=' + contract + '&apiKey=' + config.api_key['jcdecaux'], lang='json')
    else:
      xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?apiKey=' + config.api_key['jcdecaux'], lang='json')
    dic = {}
    for sta in xml.data.json.find_all("item", recursive=False):
      dic[sta.contract_name.string.lower() + '_' + sta.number.string] =\
        sta.find('name').string + ' (' + sta.address.get_text() + ')'
      # we use find('name') because .name is the current tag name
  else:
    raise ValueError('mauvaise réponse !')

  # find an id in dic
  while True:
    pat = input('Rechercher (ctrl+c pour quitter) : ').lower()
    print('Correspondances :')
    for key, value in dic.items():
      if pat in value.lower():
        print(key + ' :\t' + value)

find_id()
