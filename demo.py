from geocoding import *
import webbrowser
import main
import notification
import tempfile
import os

def str_of_pos(pos):
  return '{lat: ' + str(pos[0]) + ', lng: ' + str(pos[1]) + '}'

def escape(str):
  return str.replace("'", "\\'")

def str_of_marker(pos, description):
  return """
  marker = new google.maps.Marker({
    position: """ + str_of_pos(pos) + """,
    map: map,
    title: '""" + escape(description) + """'
  });
  var infowindow = new google.maps.InfoWindow({
    content: '""" + escape(description) + """'
  });
  infowindow.open(marker.get('map'), marker);"""


def open_markers(center, location, markers):
  if input('Montrer la carte ? [Y/n] ') != 'n':
    html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
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
""" + str_of_marker(center, 'Destination : ' + location)
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
    os.write(f, html.encode('utf-8'))
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
    markers = []

    for source in main.gen_sources(sourceProviders, location):
        if source.problem():
            print("Problème : ", end='')
        else:
            print("Pas de problème : ", end='')
        notification.notify(source.message)
        markers.append((source.pos, source.name))

    open_markers(position, location, markers)

  # empty line
  print()
