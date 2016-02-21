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

def k_neighbors(positions, fro, n):
  """returns a list of (dist, id) of the n nearest points from fro
  positions is a dictionary id -> (lat, long)"""
  distances = sorted([(dist(fro, pos), id) for (id, pos) in positions.items()])
  return distances[:n]
