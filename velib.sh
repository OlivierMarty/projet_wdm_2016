#!/bin/bash

source ./conf.sh

velib_url="http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=status&refine.status=OPEN&rows=10" # TODO augmenter rows

velib_json=$(wget "$velib_url" -O -)
velib_xml=$(./xml2json.py -t json2xml <<< "$velib_json")
echo "$velib_xml"
#xquery_html -q:query_velib -s:"$velib_xml"
