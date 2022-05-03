import json
import os
from discord_webhook import DiscordWebhook
from app import configuration as C


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'ZTPi'
}


def notify_discord(msg):
    url = 'https://discordapp.com/api/webhooks/764566548975190026/V1Mn2Bq9et-WsKrFuJHZ35yy-lpDBrhB3IWtE9vI2pxNSJyxXU0TVGX0uSCzSS2aMiea'
    webhook = DiscordWebhook(url, content=json.dumps(msg))
    response = webhook.execute()


def notify_syslog(msg):
    print(msg)
    with open(os.path.join(C.CACHE_DIR, C.LOG_FILENAME), "a+") as fh:
        fh.write("\n") 
        fh.write(msg)
    os.chmod(C.CACHE_DIR + C.LOG_FILENAME, 0o777)
