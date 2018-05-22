#!/usr/bin/env python3

import time
import requests
import telebot

SOURCE = '' #your gelbooru/yandere/etc source in json format
BOT_TOKEN = '' #your token
CHAT_ID = '' #your chat_id
LAST_POSTED = 'src'

def download_file(url):
    r = requests.get(url, stream=True)
    with open('temp', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def post_image(image_source, original_source):
    if int(requests.get(image_source).headers['content-length']) < 5242880:
        bot.send_photo(CHAT_ID, image_source, original_source)
    else:
        download_file(image_source)
        with open('temp', 'rb') as f:
            bot.send_photo(CHAT_ID, f.read(), original_source) 
    time.sleep(1)

bot = telebot.TeleBot(BOT_TOKEN)

while True:
    data = requests.get(SOURCE).json()
    last_image_source = data[0]['file_url']

    try:
        with open(LAST_POSTED, 'r') as f:
            last_posted_image = f.read()
    except FileNotFoundError:
        post_image(data[0]['file_url'], data[0]['source'])
        with open(LAST_POSTED, 'w') as f:
            f.write(data[0]['file_url'])
        
        with open(LAST_POSTED, 'r') as f:
            last_posted_image = f.read()

    if last_image_source != last_posted_image:
        try:
            for i in range(0, 100):
                if data[i]['file_url'] == last_posted_image:
                    current_number = i

            for i in range(current_number - 1, -1, -1):
                post_image(data[i]['file_url'], data[i]['source'])
        except NameError:
            current_number = 1

            for i in range(current_number - 1, -1, -1):
                post_image(data[i]['file_url'], data[i]['source'])

        with open(LAST_POSTED, 'w') as f:
            f.write(last_image_source)
    else:
        print('Zzz... {}'.format(time.strftime('%X %x')))
        time.sleep(3600)
