#!/bin/bash

source ./conf.sh
source ./ratp.sh
source ./notification.sh

traffic=$(xquery_html -q:query_ratp_traffic -s:"http://www.ratp.fr/meteo/")
traffic_ligne_7=$(xquery -qs:"//ligne[@id='ligne_metro_7']" -s:- <<< "$traffic")
statut=$(xquery -qs:"/ligne/normal/text()" -s:- \!omit-xml-declaration=yes <<< "$traffic_ligne_7")
if [ "$statut" = "true" ]
then
  message=$(xquery -qs:"/ligne/message/text()" -s:- \!omit-xml-declaration=yes <<< "$traffic_ligne_7")
  notify "Problème sur la ligne 7 : $message"
fi
