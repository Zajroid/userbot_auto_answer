import vk
import time
import random
import json
import requests 
import lxml

from distutils.command.config import config
from configparser import ConfigParser
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep
from bs4 import BeautifulSoup 
from vk.exceptions import VkAPIError
from loguru import logger


config = ConfigParser()
config.read('./systemd/config.ini')

logger.add('./logs/logers.log', 
           format="{time} {level} {message}",
           level="INFO", 
           rotation="1 MB", 
           compression="zip")


NAME = config.get('pyrogram', 'name')
API_ID = config.get('pyrogram', 'api_id')
API_HASH = config.get('pyrogram', 'api_hash')
PHONE_NUMBER = config.get('pyrogram', 'phone_number')

TOKEN_VK = config.get('vk', 'token')
OPEN_WEATHER_MAP_KEY = config.get('openweathermap', 'OPEN_WEATHER_MAP_KEY')

# print(NAME, API_ID, API_HASH, PHONE_NUMBER, TOKEN_VK, OPEN_WEATHER_MAP_KEY, sep="\n")


app = Client(name=NAME, 
             api_id=API_ID, 
             api_hash=API_HASH, 
             phone_number=PHONE_NUMBER)


# ask
greeting_dict = ['hi', 'привет', 'даров', 'ку', 'ку-ку', 'hello', 'здравствуйте']
fatewell_dict = ['пока', 'bye', 'поки', 'досвидания', 'бай', 'до скорого']

# answer
greeting_answer_list = ['даров', 'ку', 'привет', 'здравствуйте', 'вассап']
fatewell_answer_list = ['досвидания', 'пока', 'бай', 'увидимся']

# how are you???
how_are_doing_list = ['как дела?', 'как дела', 'как ты', 'how are do?', 'how are doing?', 'how you']
how_are_doing_answer_list = ['нормально, а ты?', 'отлично, а ты?', 'пойдет', 'та как обычно, ты?']

# IDK
idk_answer_list = ['я не знаю ответа', 'я просто цифры', 'не шарю', 'и что это?', '-_-']

# punctuation
punctuation_list = ['?',',','.','...',':',';','#','$']
punctuation_answer_list = ['???']


class VK(object):
    def parsing_vk(self):
        api = vk.API(access_token=str(TOKEN_VK).strip('\"'), v='5.131')
        posts = api.wall.get(domain="english_with_pleasure", count=1)
        for i in posts['items']:
            return str(i['text'])


def parsing_test():
    response = requests.get("https://duckduckgo.com/") 
    soup = BeautifulSoup(response.content, 'html.parser') 
    return soup.title.string


def parsing_english_native():
    r = requests.get('https://www.native-english.ru/grammar')
    soup = BeautifulSoup(r.content, 'lxml')

    list_links = soup.find_all('li', attrs={"class": "list__item"})
    test = []
    counter = 0

    for i in list_links:
        if counter > 20:
            break
        else:
            link_a = i.findNext('a', attrs={"itemprop": "item"})
            link_articles_title = link_a.get("title")
            link_articles = "https://www.native-english.ru" + link_a.get("href")
            test.append(f"{link_articles_title}: {link_articles}")
            counter += 1
        
    return str(test)


@app.on_message(filters=filters.dice & filters.incoming & filters.private)
async def dice(client, message):
    player_1 = message # usr
    player_2 = (await app.send_dice(message.chat.id)) # bot

    await sleep(3.5)

    if player_1.dice.value > player_2.dice.value:
        await app.send_message(message.chat.id, 'Ты выиграл!')
    elif player_1.dice.value < player_2.dice.value:
        await app.send_message(message.chat.id, 'Ты проиграл')
    else:
        await app.send_message(message.chat.id, 'Ничья')
        

@app.on_message(filters=filters.private & filters.incoming & filters.text)
async def auto_answer(client: Client, message: Message):
    if message.text.lower() in greeting_dict:
        await app.send_message(message.chat.id, random.choice(greeting_answer_list).capitalize())
    elif message.text.lower() in fatewell_dict:
        await app.send_message(message.chat.id, random.choice(fatewell_answer_list).capitalize())
    elif message.text.lower() in how_are_doing_list:
        await app.send_message(message.chat.id, random.choice(how_are_doing_answer_list).capitalize())
    elif message.text.lower() in punctuation_list:
        await app.send_message(message.chat.id, random.choice(punctuation_answer_list).capitalize())
    elif message.text.lower() == "$cat":
        await client.send_sticker(chat_id=message.chat.id, sticker='tgbot/stickers/sticker.webp')
    elif message.text.lower() == "что делаешь?":
        await client.send_sticker(chat_id=message.chat.id, sticker='tgbot/stickers/cats/i_busy.webp')
        time.sleep(0.5)
        await client.send_message(message.chat.id, 'busy')
    else:
        await app.send_message(message.chat.id, random.choice(idk_answer_list).capitalize())


@app.on_message(filters.command('pars_vk', prefixes='$'))
async def auto_answer(client: Client, message: Message):
    try:
        vk = VK()
        logger.info(f"Message has been send {message.chat.id}")
        await app.send_message(message.chat.id, vk.parsing_vk())
    except Exception as e:
        logger.error(f"{e}")
        await app.send_message(message.chat.id, "Не сейчас")
        
@app.on_message(filters=filters.voice)
async def ddd(client: Client, message: Message):
    try:
        await app.download_media(message)
        await app.send_message(message.chat.id, "voice?")
    except Exception as e:
        logger.error(f"{e}")
        await app.send_message(message.chat.id, "error")


@app.on_message(filters.command('pars', prefixes='$'))
async def auto_answer(client: Client, message: Message):
    ddd = parsing_test()
    await app.send_message(message.chat.id, ddd)
    
    
@app.on_message(filters.command('preng', prefixes='$'))
async def auto_answer(client: Client, message: Message):
    ddd = parsing_english_native()
    await app.send_message(message.chat.id, ddd, disable_web_page_preview=True)


@app.on_message(filters=filters.command('vc1', prefixes='.'))
async def vc1(client: Client, message: Message):
    await app.send_voice(message.chat.id, "audio_2022-10-17_11-54-05.ogg")
    

@app.on_message(filters=filters.command('vc2', prefixes='.'))
async def vc1(client: Client, message: Message):
    await app.send_voice(message.chat.id, "audio_2022-10-17_11-54-05.ogg")
    
    
@app.on_message(filters=filters.command('vc3', prefixes='.'))
async def vc1(client: Client, message: Message):
    await app.send_voice(message.chat.id, "audio_2022-10-17_11-54-05.ogg")


if __name__=='__main__':
    app.run()
