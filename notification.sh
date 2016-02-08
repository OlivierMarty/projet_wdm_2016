#!/bin/bash

source ./conf.sh

# usage : notify "message"
function notify {
  case "$notification_methode" in
    free)
      curl "https://smsapi.free-mobile.fr/sendmsg"\
        --get\
        --data-urlencode user=$notification_free_user\
        --data-urlencode pass=$notification_free_pass\
        --data-urlencode msg="$@"
      ;;
    sendmail)
      mail -s "$notification_sendmail_object" "$notification_sendmail_to" <<< "$@"
      ;;
    *)
      echo "\$notification_methode=$notification_methode non reconnu !" >&2
      exit 1
  esac
}
