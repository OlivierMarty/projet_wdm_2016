#!/bin/bash

source ./conf.sh

url="http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=status&refine.status=OPEN&rows=10000"
#url="https://api.jcdecaux.com/vls/v1/stations?contract=paris&apiKey=$api_key_jcdecaux"

xml=$(wget "$url" -O - 2>/dev/null | json2xml)

xquery -q:query_jcdecaux_vls -s:- <<< "$xml"
