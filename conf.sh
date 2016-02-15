#!/bin/bash

# EVENEMENTS A SURVEILLER

events_ids="ratp_traffic_ligne_metro_7 velib_42703"


# NOTIFICATIONS

notification_method="print" # ou "free" ou "sendmail"

# méthode "free" (sms api voir http://mobile.free.fr/ )
notification_free_user="123456789"
notification_free_pass="wwwwwwwww"

# méthode "sendmail"
notification_sendmail_to="example@example.com"
notification_sendmail_object="Notification traffic"


# CONFIGURATION AVANCEE

# xquery processor
function xquery {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query $@ \!indent=yes
}
function xquery_html {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query -x:org.ccil.cowan.tagsoup.Parser $@ \!indent=yes
}

# json to xml
function json2xml {
  ./xml2json.py -t json2xml
}
