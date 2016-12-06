# -*- utf-8 -*-
# _||_ Code Test number 10 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
# import re
from API import Img
from lang import EN as en
import Config

# Bot Token taken by @BotFather
TOKEN = Config.TOKEN


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
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'], ) #triggers the message for /start command
def send_welcome(m):
    text = m.text
    cid = m.chat.id

    if text == "/start tags":
        bot.send_message(cid, en.commandText['/start tags'].format(bot_id=Config.BOT_ID), parse_mode='markdown')
    elif text == "/start source_id":
        bot.send_message(cid, en.commandText['/start source_id'], parse_mode='markdown')
    else:
        try:
            bot.reply_to(m, en.commandText['start'].format(name = m.from_user.first_name, bot_name=Config.BOT_NAME),
                     parse_mode='markdown',)
        except Exception:
            print(Exception)
            pass

@bot.message_handler(commands=['help'])
def send_help(m):
    try:
        bot.reply_to(m, en.commandText['help'], parse_mode='markdown')
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['commands'])
def send_commands(m):
    try:
        bot.reply_to(m, en.commandText['commands'].format(bot_id=Config.BOT_ID), parse_mode='markdown')
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    try:
        bot.reply_to(m, en.commandText['inline_help'].format(bot_id=Config.BOT_ID), parse_mode='markdown')
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['anime'])
def send_anime(m):
    cid = m.chat.id
    load = Img.anime()
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    width = load[9]
    height = load[10]
    tag = load[1]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='anime')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,tag=tag,),
                       reply_markup=keyboard)  # reply_markup=keyboard
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /anime:", Exception)
        pass

@bot.message_handler(commands=['ecchi'])
def send_ecchi(m):
    cid = m.chat.id
    load = Img.ecchi()
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    width = load[9]
    height = load[10]
    tag = load[1]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='ecchi')
    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,tag=tag,),
                       reply_markup=keyboard)  # reply_markup=keyboard
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /ecchi:", Exception)
        pass

@bot.message_handler(commands=['loli'])
def send_loli(m):
    cid = m.chat.id
    load = Img.loli()
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    width = load[9]
    height = load[10]
    tag = load[1]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='loli')
    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,tag=tag,),
                       reply_markup=keyboard)  # reply_markup=keyboard
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /loli:", Exception)
        pass

@bot.message_handler(commands=['hentai'])
def send_hentai(m):
    cid = m.chat.id
    load = Img.hentai()
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    width = load[9]
    height = load[10]
    tag = load[1]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='hentai')
    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,tag=tag,),
                       reply_markup=keyboard)  # reply_markup=keyboard
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /hentai:", Exception)
        pass

@bot.message_handler(commands=['yuri'])
def send_yuri(m):
    cid = m.chat.id
    load = Img.yuri()
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    width = load[9]
    height = load[10]
    tag = load[1]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='yuri')
    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,tag=tag,),
                       reply_markup=keyboard)  # reply_markup=keyboard
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /yuri:", Exception)
        pass

@bot.message_handler(commands=['cosplay', 'ecosplay','id','tag'])
def send_nonworking_message(m):
    bot.reply_to(m, 'This command is not available yet :(')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message: # procees only buttons from messages
        if call.data == "anime":
            load = Img.anime()
            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            width = load[9]
            height = load[10]
            tag = load[1]
            uploader = load[3]


            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="💾 Download",url=big_picture)
            button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='anime')

            try:
                keyboard.add(button)
                keyboard.add(button2)

                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, picture,
                               caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                         uploader=uploader,
                                                                                                         tag=tag,),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred in 'more anime':", Exception)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "ecchi":
            load = Img.ecchi()
            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            width = load[9]
            height = load[10]
            tag = load[1]
            uploader = load[3]

            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="💾 Download",url=big_picture)
            button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='ecchi')

            try:
                keyboard.add(button)
                keyboard.add(button2)

                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, picture,
                                caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,
                                                                                                          tag=tag,),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred in 'more ecchi':", Exception)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "loli":
            load = Img.loli()
            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            width = load[9]
            height = load[10]
            tag = load[1]
            uploader = load[3]

            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="💾 Download",url=big_picture)
            button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='loli')

            try:
                keyboard.add(button)
                keyboard.add(button2)

                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, picture,
                                caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,
                                                                                                          tag=tag,),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred in 'more loli':", Exception)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "hentai":
            load = Img.hentai()
            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            width = load[9]
            height = load[10]
            tag = load[1]
            uploader = load[3]

            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="💾 Download",url=big_picture)
            button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='hentai')

            try:
                keyboard.add(button)
                keyboard.add(button2)

                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, picture,
                                caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,
                                                                                                          tag=tag,),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred in 'more hentai':", Exception)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "yuri":
            load = Img.yuri()
            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            width = load[9]
            height = load[10]
            tag = load[1]
            uploader = load[3]

            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="💾 Download",url=big_picture)
            button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='yuri')

            try:
                keyboard.add(button)
                keyboard.add(button2)

                bot.send_chat_action(call.message.chat.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, picture,
                                caption='🖥Resolution: {W} x {H}\n\n👤Uploader: {uploader}\n\n#⃣Tags: {tag}'.format(H=height, W=width,
                                                                                                          uploader=uploader,
                                                                                                          tag=tag,),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred in 'more yuri':", Exception)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass

@bot.inline_handler(lambda query: query.query == 'Hi') #useless?
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('LOL'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Yo'))
        r3 = types.InlineQueryResultArticle('3', 'Try Hard', types.InputTextMessageContent('_Tryharding_', parse_mode='markdown'))
        bot.answer_inline_query(inline_query.id, [r, r2, r3])
    except Exception as e:
        print("An error Ocurred:", e)

@bot.message_handler(func=lambda message: True) #Handling keyboard buttons
def keyboard(m):
    text = m.text

    if text == "1. Test":
        bot.reply_to(m, en.keyboard['Test'].format(name=m.from_user.first_name), parse_mode='markdown')
    elif text == "2. Test":
        bot.reply_to(m, en.keyboard['Test2'].format(name=m.from_user.first_name), parse_mode='markdown')

def main_loop():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
        else:
            break
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)
