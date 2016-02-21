import config
from class_xml import XML
from source import *


def find_id():
  t = int(input('Sélectionnez la source :\n\t1 : ratp\n\t2 : transilien\n\t3 : jcdecaux_vls (vélos en libre service)\n'))
  if t == 1: # RATP
    dic = SourceProvider_ratp().dic_of_names()

  elif t == 2: # transilien
    dic = SourceProvider_transilien().dic_of_names()

  elif t == 3: # jcdecaux_vls
    print('Téléchargment de la liste des villes...')
    xml_contracts = XML(url='https://api.jcdecaux.com/vls/v1/contracts?apiKey=' + config.api_key['jcdecaux_vls'], lang='json')
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
    dic = SourceProvider_jcdecaux_vls().dic_of_names(contract)
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
