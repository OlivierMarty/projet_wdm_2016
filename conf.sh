#!/bin/bash

# NOTIFICATIONS
notification_methode="sendmail" # ou "free"

# méthode "free" (sms api voir http://mobile.free.fr/ )
notification_free_user="12345678"
notification_free_pass="wwwwwwwwwww"

# méthode "sendmail"
notification_sendmail_to="example@example.com"
notification_sendmail_object="Notification traffic"

# xquery processor
function xquery {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query $@ \!indent=yes
}
function xquery_html {
  java -cp saxon.jar:tagsoup-1.2.jar net.sf.saxon.Query -x:org.ccil.cowan.tagsoup.Parser $@ \!indent=yes
}
