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
  """returns a list of (dist, pos, id) of the nearest points from fro
  returns n points (if possible) and all points closer than 1.5 times the distance
  with the closest point.
  positions is a dictionary id -> (lat, long)"""
  if not positions:
    return []
  distances = []
  for (id, pos) in positions.items():
    (dmin, pmin) = min(map(lambda p : (dist(fro, p), p), pos))
    distances.append((dmin, pmin, id))
  dmin = min([d for (d, __, __) in distances])
  return list(set(sorted(distances)[:n]) | set(filter(lambda i: i[0] <= dmin+0.1, distances)))
