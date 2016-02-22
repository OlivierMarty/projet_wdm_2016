from geocoding import *
import webbrowser
import main
import notification
import tempfile
import os

def str_of_pos(pos):
  return '"' + str(pos[0]) + ',' + str(pos[1]) + '"'


sourceProviders = [SourceProvider_ratp(),
  SourceProvider_jcdecaux_vls(),
  SourceProvider_transilien()]

dic_inv = {}
for sp in sourceProviders:
    dic = sp.dic_of_positions()
    for (id, pos) in dic.items():
        for p in pos:
            if not p in dic_inv:
              dic_inv[p] = set()
            dic_inv[p].add(id)

print("position,noms")
for (pos, ids) in dic_inv.items():
    print(str_of_pos(pos) + ',"' + ";".join(ids) + '"')
