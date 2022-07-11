import json
import os
import requests
from discord_webhook import DiscordWebhook
from app import configuration as C


def notify_im(msg):
    # Discord
#    url = 'https://discordapp.com/api/webhooks/[URL]'
#    headers = {
#        'Content-Type': 'application/json',
#        'Accept': 'application/json',
#        'User-Agent': 'ZTPi'
#        }
#    webhook = DiscordWebhook(url, content=json.dumps(msg))
#    response = webhook.execute()
    # WebEx
#    url = 'https://webexapis.com/v1/webhooks/incoming/[URL]'
#    header = {
#        'Content-Type': 'application/json'
#        }
#    data = {
#        'text': msg
#        }
#    response = requests.post(url,headers=header,data=json.dumps(data))
    # Without IM
    pass



def notify_syslog(msg):
    print(msg)
    with open(os.path.join(C.LOG_DIR, C.LOG_FILENAME), "a+") as fh:
        fh.write("\n") 
        fh.write(msg)
    os.chmod(C.CACHE_DIR + C.LOG_FILENAME, 0o777)
