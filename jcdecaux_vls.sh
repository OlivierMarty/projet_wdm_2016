#!/bin/bash

source ./conf.sh

url="https://api.jcdecaux.com/vls/v1/stations?contract=paris&apiKey=$api_key_jcdecaux"

json=$(wget "$url" -O - 2>/dev/null)
xml=$(echo '{"records":' "$json" '}' | json2xml)

xquery -q:query_jcdecaux_vls -s:- <<< "$xml"
