#!/bin/bash

# NOTIFICATIONS
notification_methode="free"

# free sms api http://mobile.free.fr/
notification_free_user=""
notification_free_pass=""

# xquery processor
function xquery {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query $@ \!indent=yes
}
function xquery_html {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query -x:org.ccil.cowan.tagsoup.Parser $@ \!indent=yes
}
