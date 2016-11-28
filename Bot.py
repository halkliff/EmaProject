# _||_ Code Test number 1 in utf-8 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
import re
from API import Img
from lang import BotLangEN

# Bot Token taken by @BotFather
TOKEN = 'TOKEN'


# Listener to see when new messages arrives
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)  # register bot token
bot.set_update_listener(listener)  # register listener

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'], ) #triggers the message for /start command
def send_welcome(m):
    bot.reply_to(m, BotLangEN.commandText['start'].format(name = m.from_user.first_name), parse_mode='markdown')

@bot.message_handler(commands=['anime'])
def send_anime(m):
    cid = m.chat.id
    picture = Img.Danbooru + Img.file_url
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="Original {H} x {W}".format(H = Img.image_height, W = Img.image_width),
                                                callback_data='large_file_url')
    keyboard.add(button)

    bot.send_chat_action(cid, 'upload_photo')
    bot.send_photo(cid, picture, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message: # procees only buttons from messages
        if call.data == "large_file_url":
            large_file_url = Img.Danbooru + Img.large_file_url
            bot.send_photo(call.message.from_user.id, large_file_url)

def main_loop():
    bot.polling(none_stop=True, interval=0, timeout=3)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)
