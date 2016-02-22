from geocoding import *
import webbrowser
import main
import notification

def open_pos(pos):
  pos_str = '(' + str(pos[0]) + ', ' + str(pos[1]) + ')'
  if input('Montrer la position ' + pos_str + ' ? [Y/n] ') != 'n':
    webbrowser.open_new("https://www.google.fr/maps/search/" + pos_str)

def message():
  yield("Faisons un essai !\n")
  yield("Encore une fois ?\n")
  yield("Pas fatigués ?\n")
  while True:
    yield("")

sourceProviders = [SourceProvider_ratp(),
  SourceProvider_jcdecaux_vls(),
  SourceProvider_transilien()]

for m in message():
  print(m)
  location = input("Adresse : ")
  position = position_of_location(location)
  if not position:
    print("Désolé, l'adresse n'est pas reconnue :-(")
  else:
    open_pos(position)

    for source in main.gen_sources(sourceProviders, location):
        if source.problem():
            print("Problème : ", end='')
        else:
            print("Pas de problème : ", end='')
        notification.notify(source.message)
        if "full" in source.id:
            pos = sourceProviders[1].dic_of_positions()[source.id][0]
            open_pos(pos)

  # empty line
  print()
