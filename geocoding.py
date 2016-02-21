from geopy.geocoders import Nominatim
from geopy.distance import vincenty


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
p2 = position_of_location("Université paris diderot")
print(p1, p2, dist(p1, p2))
