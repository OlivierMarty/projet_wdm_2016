#!/bin/bash

source ./conf.sh

velib_url="http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&facet=banking&facet=status&refine.status=OPEN&rows=10000"

velib_xml=$(wget "$velib_url" -O - | json2xml)

xquery -q:query_velib -s:- <<< "$velib_xml"
