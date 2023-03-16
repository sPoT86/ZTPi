import json
import os
import requests
from app import configuration as C


def notify_im(msg):
    try:
        # Discord
        url = 'https://discordapp.com/api/webhooks/<URL>'
        data = {
            'content': msg,
            'username': 'ZTPi'
            }
        response = requests.post(url,json=data)
        # WebEx
#        url = 'https://webexapis.com/v1/webhooks/incoming/<URL>'
#        header = {
#            'Content-Type': 'application/json'
#            }
#        data = {
#            'text': msg
#            }
#        response = requests.post(url,headers=header,data=json.dumps(data))
    except Exception:
        pass
    # Without IM
    pass


def notify_syslog(msg):
    with open(os.path.join(C.LOG_DIR, C.LOG_FILENAME), "a+") as fh:
        fh.write("\n") 
        fh.write(msg)
    os.chmod(C.LOG_DIR + C.LOG_FILENAME, 0o777)
