import source
import config
import notification
from itertools import chain

sources=chain(source.ratp_trafic(), source.transilien(), source.jcdecaux_vls())

for source in sources:
  if source.id in config.sources.get(source.source, []):
    if source.problem():
      notification.notify(source.message)
