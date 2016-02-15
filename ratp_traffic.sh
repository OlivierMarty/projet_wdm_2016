#!/bin/bash

source ./conf.sh

xquery_html -q:query_ratp_traffic -s:"http://www.ratp.fr/meteo/"
