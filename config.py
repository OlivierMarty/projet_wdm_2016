

api_key = {
  'jcdecaux' : ''
}


# SOURCES D'EVENEMENTS A SURVEILLER

sources = {
  'ratp_trafic' : ['ligne_rer_B', 'ligne_metro_7'],
  'transilien' : ['RER-B', 'RER-C', 'Train-U'],
  'jcdecaux_vls' : ['paris_42707_full', 'paris_42707_empty', 'paris_42703_empty', 'paris_19001_full', 'paris_8038_empty', 'nantes_62_full']
}

# NOTIFICATIONS

notification = {
  'methods' : ['print'], # "free", "sendmail"
  'free' : { # méthode "free" (sms api voir http://mobile.free.fr/ )
    'user' : '123456789',
    'pass' : 'wwwwwwwww'
  },
  'sendmail' : { # méthode "sendmail"
    'to' : 'example@example.com',
    'object' : 'Notification trafic'
  }
}
