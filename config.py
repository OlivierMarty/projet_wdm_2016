

api_key = {
  'jcdecaux' : ''
}


# EVENEMENTS A SURVEILLER

events = {
  'ratp_traffic' : ['ligne_metro_7'],
  'jcdecaux_vls' : ['42707_full', '42707_empty']
}

# NOTIFICATIONS

notification = {
  'method' : 'print', # ou "free" ou "sendmail"
  'free' : { # méthode "free" (sms api voir http://mobile.free.fr/ )
    'user' : '123456789',
    'pass' : 'wwwwwwwww'
  },
  'sendmail' : { # méthode "sendmail"
    'to' : 'example@example.com',
    'object' : 'Notification traffic'
  }
}
