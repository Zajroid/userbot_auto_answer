import vk
import time
import random
import json
import requests 

from distutils.command.config import config
from configparser import ConfigParser
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep
from bs4 import BeautifulSoup 
from vk.exceptions import VkAPIError


config = ConfigParser()
config.read('./systemd/config.ini')


NAME = config.get('pyrogram', 'name')
API_ID = config.get('pyrogram', 'api_id')
API_HASH = config.get('pyrogram', 'api_hash')
PHONE_NUMBER = config.get('pyrogram', 'phone_number')

TOKEN_VK = config.get('vk', 'token')
OPEN_WEATHER_MAP_KEY = config.get('openweathermap', 'OPEN_WEATHER_MAP_KEY')


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


def parsing_vk():
    api = vk.API(access_token=str(TOKEN_VK).strip('\"'), v='5.131')

    posts = api.wall.get(domain="english_with_pleasure", count=1)

    print(posts.items())

    for i in posts['items']:
        return str(i['text'])


def parsing_test():
    response = requests.get("https://duckduckgo.com/") 
    soup = BeautifulSoup(response.content, 'html.parser') 
        
    return soup.title.string



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
        

@app.on_message(filters=filters.private & filters.incoming & filters.regex('[а-яА-Яa-zA-z]'))
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


@app.on_message(filters=filters.private & filters.outgoing & filters.regex('[а-яА-Яa-zA-z]') & filters.command('$pars_vk'))
async def auto_answer(client: Client, message: Message):
    if message.text.lower() == "$pars":
        prs_test = parsing_test()
        await app.send_message(message.chat.id, prs_test)
    else:
        await app.send_message(message.chat.id, 'не вышло(')


@app.on_message(filters=filters.private & filters.outgoing & filters.regex('[а-яА-Яa-zA-z]') & filters.command('$pars') )
async def auto_answer(client: Client, message: Message):
    prs_vk = parsing_vk()
    await app.send_message(message.chat.id, prs_vk)


@app.on_message(filters=filters.private & filters.incoming)
async def auto_answer(client: Client, message: Message):    
    if message.text.lower() == "123":
        await app.send_message(message.chat.id, "321")


if __name__=='__main__':
    app.run()
