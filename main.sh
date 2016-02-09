#!/bin/bash

source ./conf.sh
source ./notification.sh

traffic=$(xquery_html -q:query_ratp_traffic -s:"http://www.ratp.fr/meteo/")
traffic_ligne_7=$(xquery -qs:"/results/result[id/text()='ratp_traffic_ligne_metro_7']" -s:- <<< "$traffic")
statut=$(xquery -qs:"/result/status/text()" -s:- \!omit-xml-declaration=yes <<< "$traffic_ligne_7")
if [ "$statut" = "problem" ]
then
  message=$(xquery -qs:"/result/message/text()" -s:- \!omit-xml-declaration=yes <<< "$traffic_ligne_7")
  notify "Problème sur la ligne 7 : $message"
fi
