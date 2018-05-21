#!/usr/bin/env python3

import time
from os.path import isfile

import requests
import telebot

SOURCE = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=loli+-animated&json=1'
BOT_TOKEN = '' #your token
CHAT_ID = '' #your chat_id
LAST_POSTED = 'src'

def json_parse(source, image_number):
    data = []
    response = requests.get(source)
    image_source = response.json()[image_number]['file_url']
    original_source = response.json()[image_number]['source']
    data.append(image_source)
    data.append(original_source)
    return data

def post_image(image_source, original_source):
    bot.send_photo(CHAT_ID, image_source, original_source)
    time.sleep(1)

bot = telebot.TeleBot(BOT_TOKEN)

if not isfile(LAST_POSTED):
    post_image(json_parse(SOURCE, 0)[0], json_parse(SOURCE, 0)[1])
    with open(LAST_POSTED, 'w') as f:
        f.write(json_parse(SOURCE, 0)[0])

while True:
    last_image_source = json_parse(SOURCE, 0)[0]
    with open(LAST_POSTED, 'r') as f:
        last_posted_image = f.read()

    if last_image_source != last_posted_image:
        for i in range(0, 99):
            if last_posted_image == json_parse(SOURCE, i)[0]:
                current_number = i
                break

        if current_number == None:
            current_number = 1

        for i in range(current_number - 1, -1, -1):
            post_image(json_parse(SOURCE, i)[0], json_parse(SOURCE, i)[1])
        with open(LAST_POSTED, 'w') as f:
            f.write(last_image_source)
    else:
        print('Zzz... {}'.format(time.strftime('%X %x')))
        time.sleep(3600)
