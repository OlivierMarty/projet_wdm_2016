from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from source import *


geolocator = Nominatim()


def position_of_location(location):
    """returns a pair (latitude, longitude) from an adress
    or None if not possible"""
    try:
      pos = geolocator.geocode(location)
      return (pos.latitude, pos.longitude)
    except:
      return None

def dist(posa, posb):
    """compute the distance between two position (pair latitude, longitude)
    in kilometers
    or None if one of the argument is None"""
    if not posa or not posb:
        return None
    else:
        return vincenty(posa, posb).km

p1 = position_of_location("22 rue Henri Barbusse VILLEJUIF")
#p2 = position_of_location("Université paris diderot")
#print(p1, p2, dist(p1, p2))


def k_neighbors(positions, fro, n):
  """returns a list of (dist, id) of the n nearest points from fro
  positions is a dictionary id -> (lat, long)"""
  distances = sorted([(dist(fro, pos), id) for (id, pos) in positions.items()])
  return distances[:n]

res = k_neighbors(SourceProvider_jcdecaux_vls().dic_of_positions(), p1, 5)
names = SourceProvider_jcdecaux_vls().dic_of_names()
for (dist, id) in res:
  print(names[id] + ' at ' + str(dist) + 'km')
