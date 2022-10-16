from string import punctuation
import time
import random

from distutils.command.config import config
from configparser import ConfigParser
from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep


config = ConfigParser()
config.read('./systemd/config.ini')


name = config.get('pyrogram', 'name')
api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')
phone_number = config.get('pyrogram', 'phone_number')


app = Client(name=name, 
             api_id=api_id, 
             api_hash=api_hash, 
             phone_number=phone_number)


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
    mci = message.chat.id
    
    if message.text.lower() in greeting_dict:
        await app.send_message(mci, random.choice(greeting_answer_list).capitalize())
    elif message.text.lower() in fatewell_dict:
        await app.send_message(mci, random.choice(fatewell_answer_list).capitalize())
    elif message.text.lower() in how_are_doing_list:
        await app.send_message(mci, random.choice(how_are_doing_answer_list).capitalize())
    elif message.text.lower() in punctuation_list:
        await app.send_message(mci, random.choice(punctuation_answer_list).capitalize())
    elif message.text.lower() == "$cat":
        await client.send_sticker(chat_id=mci, sticker='tgbot/stickers/sticker.webp')
    elif message.text.lower() == "что делаешь?":
        await client.send_sticker(chat_id=mci, sticker='tgbot/stickers/cats/i_busy.webp')
        time.sleep(0.5)
        await client.send_message(mci, 'busy')
    else:
        await app.send_message(mci, random.choice(idk_answer_list).capitalize())


@app.on_message(filters=filters.private & filters.incoming)
async def auto_answer(client: Client, message: Message):
    mci = message.chat.id
    
    if message.text.lower() == "123":
        await app.send_message(mci, "321")


if __name__=='__main__':
    app.run()
