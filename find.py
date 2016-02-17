import config
from class_xml import XML


def find_id():
  t = input('selectionnez\n\t1 : ratp\n\t2 : jcdecaux_vls (velib)\n')
  if int(t) == 1:
    print('Télechargement de la liste des lignes...')
    xml = XML(url='http://www.ratp.fr/meteo/', lang='html')
    dic = {tag['id']: tag['id'].replace('_', ' ') for tag in xml.data.select('.encadre_ligne')}
  elif int(t) == 2:
    print('Télechargement de la liste des stations...')
    xml = XML(url='https://api.jcdecaux.com/vls/v1/stations?contract=paris&apiKey=' + config.api_key['jcdecaux'], lang='json')
    dic = {sta.number.string: sta.find('name').string + ' (' + sta.address.string + ')' for sta in xml.data.find_all("item")} # we use find('name') because .name is the current tag name
  else:
    raise ValueError('mauvaise réponsse !')

  while True:
    pat = input('Rechercher (ctrl+c pour quitter) : ').lower()
    print('Correspondances :')
    for key, value in dic.items():
      if pat in value.lower():
        print('id ' + key + ' : ' + value)

find_id()
