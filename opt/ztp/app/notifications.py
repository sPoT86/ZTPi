import json
import os
import requests
import datetime
from app import configuration as C


def notify_im(msg):
#    try:
        # Discord
#        url = 'https://discordapp.com/api/webhooks/{API-KEY}'
#        data = {
#            'content': msg,
#            'username': 'ZTPi'
#            }
#        response = requests.post(url,json=data)
        # WebEx
#        url = 'https://webexapis.com/v1/webhooks/incoming/{API-KEY}'
#        header = {
#            'Content-Type': 'application/json'
#            }
#        data = {
#            'text': msg
#            }
#        response = requests.post(url,headers=header,data=json.dumps(data))
    # IM error handling
 #   except requests.exceptions.ConnectionError as e:
 #       notify_syslog(f"IM - network error: {e}")
 #   else:
 #       if response.status_code == 200:
 #           pass
 #       elif response.status_code == 401:
 #           notify_syslog("IM error - wrong login data")
 #       elif response.status_code == 403:
 #           notify_syslog("IM error - not permitted")
 #       elif response.status_code == 404:
 #           notify_syslog("IM error - resource not found")
 #       elif response.status_code == 408:
 #           notify_syslog("IM error - timeout")
    # Without IM
    pass

    

def notify_syslog(msg):
    dtime = datetime.datetime.now()
    with open(os.path.join(C.LOG_DIR, C.LOG_FILENAME), 'a+') as fh:
        fh.write("\n")
        fh.write(f"{dtime}: {msg}")
    os.chmod(C.LOG_DIR + C.LOG_FILENAME, 0o777)

