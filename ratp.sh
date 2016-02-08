#!/bin/bash

source ./conf.sh

# usage : ratp_url_metro arret n°ligne A|R
function ratp_url_metro {
  echo "http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/"$1"/"$2"/"$3
}

# requete
$xquery_html -q:query_metro -s:"$(ratp_url_metro "republique" 5 A)"
