import csv

# sources des données : http://data.ratp.fr/explore/dataset/offre-transport-de-la-ratp-format-gtfs/

def get_stops():
  """Returns a dictionary stop_id -> (latitude, longitude)
  and a dictionary address -> list of stop_id"""
  res = {}
  res_add = {}
  with open("ratp_data/stops.txt", "r") as stops:
    for fields in csv.reader(stops, delimiter=',', quotechar='"'):
      if fields[0] != 'stop_id':
        res[fields[0]] = (fields[4], fields[5])
        if not fields[3] in res_add:
            res_add[fields[3]] = []
        res_add[fields[3]].append(fields[0])
  return (res, res_add)

def get_stop_times():
  """Returns a dictionary stop_id -> set of trip_id"""
  res = {}
  with open("ratp_data/stop_times.txt", "r") as stop_times:
    for fields in csv.reader(stop_times, delimiter=',', quotechar='"'):
      if fields[0] != 'trip_id':
        if fields[3] not in res:
           res[fields[3]] = set()
        res[fields[3]].add(fields[0])
  return res

def get_trips():
  """Returns a dictionary trip_id -> route_id"""
  res = {}
  with open("ratp_data/trips.txt", "r") as trips:
    for fields in csv.reader(trips, delimiter=',', quotechar='"'):
      if fields[0] != 'route_id':
        res[fields[2]] = fields[0]
  return res


def get_routes():
  """Returns a dictionary route_id -> route_short_name"""
  res = {}
  with open("ratp_data/routes.txt", "r") as routes:
    for fields in csv.reader(routes, delimiter=',', quotechar='"'):
      if fields[0] != 'route_id':
        res[fields[0]] = fields[2].replace('"', '')
  return res


def get_lines_of_stations(stop_times, trips, routes, id):
  """Returns a list of line passing through station [id]"""
  # get a set of trip_id using this station
  trips_set = stop_times[id]
  # get the set of route_id for these trips
  routes_set = set(map(trips.get, trips_set))
  # get the set of lines for these routes
  lines = set(map(routes.get, routes_set))
  return list(lines)

def name_to_id(name):
  """convert the name of a ligne to internal id"""
  if name == 'A' or name == 'B':
    return 'ligne_rer_' + name
  if name == 'T3': # spécial case
    return 'ligne_tram_T3a'
  if name[0] == 'T' and name[1] in map(str, range(0, 10)):
    return 'ligne_tram_' + name
  try:
    if int(name) < 20: # TODO je n'ai pas vu les métro 7bis et 3bis
      return 'ligne_metro_' + name
  except ValueError:
    pass
  return 'ligne_bus_' + name



# Each line has its own stop_id :
# we group by stop_id by address
def preprocessing():
  """Print the list of stations in the format stop_id,lat,lon,line:...:line"""
  trips = get_trips()
  routes = get_routes()
  stop_times = get_stop_times()
  (stops, stops_add) = get_stops()
  for (address, ids) in stops_add.items():
    try:
      lines = set()
      for id in ids:
        lines.add(*get_lines_of_stations(stop_times, trips, routes, id))
      (lat, lon) = stops[ids[0]] # arbitrary element, they all should have the same position
      print(lat + "," + lon + "," + ":".join(map(name_to_id, lines)))
    except KeyError:
      pass

if __name__ == "__main__":
  preprocessing()
