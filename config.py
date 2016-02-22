
# API KEYS

api_key = {
  'jcdecaux_vls' : '',
  'google_maps'  : ''
}


# PARAMÈTRES DES SOURCES D'EVENEMENTS

sources_params = {
  'jcdecaux_vls' : {
    'limit_full' : 4, # en dessous de cette limite, une notificaation est envoyée
    'limit_empty': 4  # idem
  }
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
