#!/bin/bash

source ./conf.sh
source ./notification.sh

# combine plusieurs xml de racine results sous la même racine
# usage : combine string1 string2 ...
function combine {
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<results>'
  for xml in "$@"
  do
    xquery -qs:"/results/*" -s:- \!omit-xml-declaration=yes <<< "$xml"
  done
  echo '</results>'
}

# telecharge et combine les données

echo "Download ratp_traffic..." >&2
results_ratp_traffic=$(./ratp_traffic.sh)

echo "Download velib..." >&2
results_velib=$(./velib.sh)

echo "Combine results..." >&2
results=$(combine "$results_ratp_traffic" "$results_velib")

# pour chaque evenement, envoie une notification s'il y a un problème
for id in $events_ids
do
  echo "Search result for $id..." >&2
  result=$(xquery -qs:"/results/result[id/text()='$id']" -s:- <<< "$results")
  statut=$(xquery -qs:"/result/status/text()" -s:- \!omit-xml-declaration=yes <<< "$result")
  if [ "$statut" = "problem" ]
  then
    message=$(xquery -qs:"/result/message/text()" -s:- \!omit-xml-declaration=yes <<< "$result")
    notify "$message"
  fi
done
