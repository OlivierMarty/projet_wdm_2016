from geocoding import *
import webbrowser
import main
import notification
import tempfile
import os

def str_of_pos(pos):
  return '{lat: ' + str(pos[0]) + ', lng: ' + str(pos[1]) + '}'

def str_of_marker(pos, description):
  return """
  marker = new google.maps.Marker({
    position: """ + str_of_pos(pos) + """,
    map: map,
    title: '""" + description + """'
  });
  var infowindow = new google.maps.InfoWindow({
    content: '""" + description + """'
  });
  infowindow.open(marker.get('map'), marker);"""


def open_markers(center, markers):
  # markers_str = map(lambda pos_name: '&markers=color:blue|label:' + pos_name[1] + '|' + str_of_pos(pos_name[0]) , markers)
  # if input('Montrer la carte ? [Y/n] ') != 'n':
  #   url = "http://maps.google.com/maps/api/staticmap?center" + str_of_pos(center) +\
  #   '&zoom=14&size=512x512&maptype=roadmap' +\
  #   '&markers=color:red|label:destination|' + str_of_pos(center) + ''.join(markers_str)
  #   webbrowser.open_new(url)
  if input('Montrer la carte ? [Y/n] ') != 'n':
    html = """<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      html, body { height: 100%; margin: 0; padding: 0; }
      #map { height: 100%; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script type="text/javascript">
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: """ + str_of_pos(center) + """,
    zoom: 15
  });
""" + str_of_marker(center, 'destination')
    for (pos, name) in markers:
      html += str_of_marker(pos, name)
    html += """
}
    </script>
    <script async defer
      src="https://maps.googleapis.com/maps/api/js?key=""" + config.api_key['google_maps'] + """&callback=initMap">
    </script>
  </body>
</html>"""
    (f, path) = tempfile.mkstemp(suffix=".html")
    os.write(f, html.encode())
    os.close(f)
    webbrowser.open_new('file://' + path)

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
    #open_pos(position)
    markers = []

    for source in main.gen_sources(sourceProviders, location):
        if source.problem():
            print("Problème : ", end='')
        else:
            print("Pas de problème : ", end='')
        notification.notify(source.message)
        markers.append((source.pos, source.id))

    open_markers(position, markers)

  # empty line
  print()
