import config
import urllib.request
import urllib.parse
from subprocess import run

def notify(message):
   """usage : notify("message")
   """
   conf = config.notification
   method = conf['method']
   if method == "free":
      data = urllib.parse.urlencode({
        'user' : conf['free']['user'],
        'pass' : conf['free']['pass'],
        'msg' : message
      })
      urllib.request.urlopen("https://smsapi.free-mobile.fr/sendmsg?" + data)
   elif method == 'sendmail':
      run(['mail', '-s', conf['sendmail']['object'], conf['sendmail']['to']], input=message.encode(), check=True)
   elif method == 'print':
      print(message)
   else:
      raise NotImplementedError('notification method = ' + method + ' not known !')
