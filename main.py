import requests
import time
import datetime

import config

from parsers import hn_parser, gh_parser
from already_sent import add_already_sent


BOT_API_KEY = config.BOT_API_KEY
CHANNEL_NAME = config.CHANNEL_NAME

def send(message):
    response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
                'chat_id': CHANNEL_NAME,
                'text': message['text']
            })
    if response.status_code == 200:  
        print(message['id'])              
        add_already_sent(message['id'])
    else:
        print(response.text)
    time.sleep(1)



if __name__ == "__main__":
    # print("start", datetime.datetime.now())
    for hn_article in hn_parser():
        send(hn_article)

    for gh_repo in gh_parser():
        send(gh_repo)
    # print("done", datetime.datetime.now())