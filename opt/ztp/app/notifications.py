import json
import os
import requests
from discord_webhook import DiscordWebhook
from app import configuration as C


def notify_im(msg):
    try:
        # Discord
        url = 'https://discordapp.com/api/webhooks/764566548975190026/V1Mn2Bq9et-WsKrFuJHZ35yy-lpDBrhB3IWtE9vI2pxNSJyxXU0TVGX0uSCzSS2aMiea'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'ZTPi'
            }
        webhook = DiscordWebhook(url, content=json.dumps(msg))
        response = webhook.execute()
        # WebEx
#        url = 'https://webexapis.com/v1/webhooks/incoming/Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1dFQkhPT0svYmUzMDI3OTMtZmMyNS00MTc5LTg0OGMtMGU3ZTEyOGIwN2Y5'
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
