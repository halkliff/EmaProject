# -*- utf-8 -*-
# _||_ Code Test number 10 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
from API import Img
from lang import EN as Lang
import Config
import re
# ========== Start of user database funcs ==========
from tinydb import TinyDB, Query  # database module

db = TinyDB('database/user/db.json')  # this is the path of the user database

def new_user(from_user_username, from_user_id, from_user_language, from_user_nsfw_choice):  # Func to insert user on database
    db.insert({'id': from_user_id, 'username':from_user_username, 'language': from_user_language, 'nsfw': from_user_nsfw_choice})

def user_search(from_user_id):  # Func to search user on database. Returns the dict if the user exists, and None if doesn't match
    user = Query()              # with anything. If the dict is empty, use new_user() func to register the user in the database.
    a = db.search(user.id == from_user_id)
    if len(a) >= 1:
        return a
    else:
        return None

# ========== End of user database funcs ==========

# Bot Token taken by @BotFather
TOKEN = Config.TOKEN


# Listener to see when new messages arrives

def listener(messages):

    # When new messages arrive TeleBot will call this function.

    for m in messages:
        if m.content_type == 'text':
             # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        # print(str(m))


bot = telebot.TeleBot(TOKEN)  # register bot token
bot.set_update_listener(listener)  # register listener

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])  # triggers the message for /start command
def send_welcome(m):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # button = types.KeyboardButton('1. Test')
    # button2 = types.KeyboardButton('2. Test')
    # text = m.text
    cid = m.chat.id
    match = user_search(str(m.chat.id))

    def deep_link(text):
        return text.split()[1] if len(text.split()) > 1 else None

    dp_link = deep_link(m.text)
    if dp_link:
        try:
            lang = match[0]['language']
            bot.send_message(cid, Lang.Lang[lang]['CommandText']['{0}'.format(dp_link)].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print("An Error occurred when processing command /start {0}:".format(dp_link), e)
            pass

    else:

        if not match:
            try:
                ky = types.ReplyKeyboardRemove(selective=False)
                new_user(str(m.from_user.username), str(m.chat.id), 'English', 'Yes')
                bot.reply_to(m, Lang.Lang['English']['CommandText']['start'].format(name = m.from_user.first_name, bot_name=Config.BOT_NAME),
                                parse_mode = 'markdown', reply_markup=ky)
            except Exception as e:
                raise Exception(e)
                pass
        else:
            try:
                lang = match[0]['language']
                ky = types.ReplyKeyboardRemove(selective=False)
                bot.reply_to(m, Lang.Lang[lang]['CommandText']['start_reg'].format(name=m.from_user.first_name),
                            parse_mode='markdown', reply_markup=ky)
            except Exception as e:
                print("An error occurred when processing the start_reg:",e)
                pass
"""
    if text == "/start tags":
        try:
            bot.send_message(cid, en.commandText['/start tags'].format(bot_id=Config.BOT_ID),
                             parse_mode='markdown',)
        except Exception:
            print("An Error occurred when processing command /start tags:", Exception)
            pass

    elif text == "/start source_id":
        try:
            bot.send_message(cid, en.commandText['/start source_id'], parse_mode='markdown',)
        except Exception:
            print("An Error occurred when processing command /start source_id:", Exception)

    elif text == "/start commands":
        try:
            bot.reply_to(m, en.commandText['commands'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                         disable_web_page_preview=True)
        except Exception:
            print(Exception)
            pass
"""
@bot.message_handler(commands=['help'])
def send_help(m):
    match = user_search(str(m.chat.id))
    lang = match[0]['language']

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    button = telebot.types.InlineKeyboardButton(Lang.Lang[lang]['keyboard']['inline_buttons']['help']['usg_help'],
                                                callback_data='help_use')
    button2 = telebot.types.InlineKeyboardButton(Lang.Lang[lang]['keyboard']['inline_buttons']['help']['cmnds'],
                                                 callback_data='commands')
    button3 = telebot.types.InlineKeyboardButton(Lang.Lang[lang]['keyboard']['inline_buttons']['help']['in_help'],
                                                 callback_data='inline_help')
    button4 = telebot.types.InlineKeyboardButton(Lang.Lang[lang]['keyboard']['inline_buttons']['help']['tags'],
                                                 callback_data='tags')
    button5 = telebot.types.InlineKeyboardButton(Lang.Lang[lang]['keyboard']['inline_buttons']['help']['src_id'],
                                                 callback_data='source_id')

    try:
        keyboard.add(button)
        keyboard.row(button2, button3)
        keyboard.row(button4, button5)

        bot.reply_to(m, Lang.Lang[lang]['CommandText']['help'], parse_mode='markdown', reply_markup=keyboard)
    except Exception as e:
        print("An error occurred when processing /help:", e)
        pass

@bot.message_handler(commands=[ 'admin' ])
def admin(m):
    cid = str(m.chat.id)
    master = str(Config.MASTER_ID)

    def send_to_master():
        kb = telebot.types.InlineKeyboardMarkup()
        kbbtn1 = telebot.types.InlineKeyboardButton("📈 Statistics", callback_data='stats')
        kb.add(kbbtn1)
        bot.reply_to(m, "Select one of the options below:", reply_markup=kb)

    send_to_master() if master == cid else bot.reply_to(m, 'who the fuck are you?')

@bot.message_handler(commands=['settings', 'config', 'configurate'])
@bot.message_handler(func=lambda m: m.text == '⚙ Settings')
def settings(m):
    lang = user_search(str(m.chat.id))[0]['language']

    menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['lang'])
    btn2 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['notif'])
    btn3 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['prefs'])
    #menu.row(btn1, btn2)
    #menu.add(btn3)
    menu.add(btn1)
    try:
        bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['set_opt'], reply_markup=menu)
    except Exception as e:
        print("An error occurred when processing /settings:", e)

@bot.message_handler(commands=['lang', 'language', 'lang_prefs'])
@bot.message_handler(func=lambda m: m.text == '🌐 Language')
@bot.message_handler(func=lambda m: m.text == '🌐 Idioma')
def lang(m):
    cid = m.chat.id
    match = user_search(str(cid))
    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match[0]['language']

        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        kbtn1 = types.KeyboardButton("🇧🇷 Português")
        kbtn2 = types.KeyboardButton("🇺🇸 English")
        kbtn3 = types.KeyboardButton("🇪🇸 Español")
        kbtn4 = types.KeyboardButton("🇮🇪 Italiano")
        kbtn5 = types.KeyboardButton("🇷🇺 русский")
        kbtn6 = types.KeyboardButton("🇩🇪 Deutsche")
        kb.row(kbtn1, kbtn2)
        #kb.row(kbtn3, kbtn4)
        #kb.row(kbtn5, kbtn6)
        try:
            msg = bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['Lang_pref'], parse_mode='markdown', reply_markup=kb)
            bot.register_next_step_handler(msg, chosen_lang)
        except Exception as e:
            print("An error occurred when processing 'Language Selector':", e)
            pass
def chosen_lang(m):
    cid = m.chat.id
    user = Query()
    text = m.text.split()
    try:
        db.update({'language': text[1]}, user.id == str(cid))

        k = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(m, Lang.Lang[text[1]]['keyboard']['messages']['Chosen_lang'], parse_mode='markdown', reply_markup=k)
    except Exception as e:
        bot.reply_to(m, 'Ops, something went wrong. Please try again with /lang')
        print("An error occurred when processing 'new_user_lang_register':", e)

@bot.message_handler(commands=['ping'])
def pong(m):
    bot.reply_to(m, 'Pong!')

@bot.message_handler(commands=['commands'])
def send_commands(m):
    match = user_search(str(m.chat.id))
    lang = match[0]['language']
    try:
        bot.reply_to(m, Lang.Lang[lang]['CommandText']['commands'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                     disable_web_page_preview=True)
    except Exception as e:
        print("An error occurred when processing /commands:", e)
        pass

@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    match = user_search(str(m.chat.id))
    lang = match[0]['language']
    try:
        bot.reply_to(m, Lang.Lang[lang]['CommandText']['inline_help'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                     disable_web_page_preview=True)
    except Exception as e:
        print("An Error occurred when processing command /inline_help:", e)
        pass

@bot.message_handler(commands=['anime'])
def send_anime(m):
    cid = m.chat.id
    try:
        load = Img.anime()
    except Exception:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='anime')
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                     reply_markup=retry_keyboard)
        pass

    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    id = load[0]
    uploader = load[3]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='anime')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                       reply_markup=keyboard)
    except Exception as e:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Occurred in /anime:", e)
        pass


@bot.message_handler(commands=['ecchi'])
def send_ecchi(m):
    cid = m.chat.id
    try:
        load = Img.ecchi()
    except Exception:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='ecchi')
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                     reply_markup=retry_keyboard)
        pass
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    id = load[0]
    uploader = load[3]

    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='ecchi')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture, caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                       reply_markup=keyboard)
    except Exception as e:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /ecchi:", e)
        pass


@bot.message_handler(commands=['loli'])
def send_loli(m):
    cid = m.chat.id
    try:
        load = Img.loli()
    except Exception:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='loli')
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                     reply_markup=retry_keyboard)
        pass
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    id = load[0]
    uploader = load[3]

    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='loli')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture, caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                       reply_markup=keyboard)
    except Exception as e:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /loli:", e)
        pass


@bot.message_handler(commands=['hentai'])
def send_hentai(m):
    cid = m.chat.id
    try:
        load = Img.hentai()
    except Exception:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='hentai')
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                     reply_markup=retry_keyboard)
        pass

    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    id = load[0]
    uploader = load[3]

    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='hentai')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture, caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                       reply_markup=keyboard)
    except Exception as e:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /hentai:", e)
        pass


@bot.message_handler(commands=['yuri'])
def send_yuri(m):
    cid = m.chat.id
    try:
        load = Img.yuri()
    except Exception:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='yuri')
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                     reply_markup=retry_keyboard)
        pass
    picture = load[8]
    big_picture = load[7]
    if big_picture is None:
        big_picture = load[8]
    id = load[0]
    uploader = load[3]

    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="💾 Download", url=big_picture)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='yuri')

    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture, caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                       reply_markup=keyboard)
    except Exception as e:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /yuri:", e)
        pass


@bot.message_handler(commands=['cosplay', 'ecosplay','id','tag', 'inline_help'])
def send_nonworking_message(m):
    bot.reply_to(m, 'This command is not available yet :(')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message: # procees only buttons from messages
         #if call.data == "large_file_url":
          #  load = Img.anime()
           # if load[15] is None:
            #    try:
             #       bot.send_document(call.message.chat.id, load[14])
              #  except Exception:
               #     print('An Error Ocurred:', Exception)
                #    pass
            #else:
             #   try:
              #      bot.send_document(call.message.chat.id, load[15])
               # except Exception:
                #    print('An error Ocurred:', Exception)
                 #   pass
        if call.data == "anime":
            try:
                load = Img.anime()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='anime')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)
                pass

            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            id = load[0]
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
                               caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                                reply_markup=keyboard)
            except Exception as e:
                print("An error Ocurred in 'more anime':", e)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "ecchi":
            try:
                load = Img.ecchi()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='ecchi')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)
                pass

            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            id = load[0]
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
                               caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                                reply_markup=keyboard)
            except Exception as e:
                print("An error Ocurred in 'more ecchi':", e)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "loli":
            try:
                load = Img.loli()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='loli')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)
                pass

            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            id = load[0]
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
                               caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                                reply_markup=keyboard)
            except Exception as e:
                print("An error Ocurred in 'more loli':", e)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "hentai":
            try:
                load = Img.hentai()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='hentai')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)
                pass

            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            id = load[0]
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
                               caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                                reply_markup=keyboard)
            except Exception as e:
                print("An error Ocurred in 'more hentai':", e)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "yuri":
            try:
                load = Img.yuri()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='yuri')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)
                pass

            picture = load[8]
            big_picture = load[7]
            if big_picture is None:
                big_picture = load[8]
            id = load[0]
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
                               caption='🔖id:{id}\n\n👤Uploader: {uploader}'.format(id=id, uploader=uploader,),
                                reply_markup=keyboard)
            except Exception as e:
                print("An error Ocurred in 'more yuri':", e)
                bot.send_message(call.message.id, "Wasn't able to proceed your request.")
                pass
        elif call.data == "commands":
            match = user_search(str(call.message.chat.id))
            lang = match[0]['language']
            try:
                bot.send_message(call.message.chat.id, Lang.Lang[lang]['CommandText']['commands'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception as e:
                print("An error occurred when processing the inline button 'Commands':", e)
                pass
        elif call.data == "inline_help":
            match = user_search(str(call.message.chat.id))
            lang = match[0]['language']
            try:
                bot.send_message(call.message.chat.id, Lang.Lang[lang]['CommandText']['inline_help'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception as e:
                print("An Error occurred when processing inline button [Inline Help]:", e)
                pass
        elif call.data == "tags":
            match = user_search(str(call.message.chat.id))
            lang = match[0]['language']
            try:
                bot.send_message(call.message.chat.id,Lang.Lang[lang]['CommandText']['tags'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown',)
            except Exception as e:
                print("An Error occurred when processing inline button [Tags]:", e)
                pass
        elif call.data == "source_id":
            match = user_search(str(call.message.chat.id))
            lang = match[0]['language']
            try:
                bot.send_message(call.message.chat.id, Lang.Lang[lang]['CommandText']['source_id'], parse_mode='markdown',)
            except Exception as e:
                print("An Error occurred when processing inline button [Source ID]:", e)
                pass
        elif call.data == "help_use":
            match = user_search(str(call.message.chat.id))
            lang = match[0]['language']
            try:
                bot.send_message(
                    call.message.chat.id, Lang.Lang[lang]['CommandText']['help_use'].format(name=call.from_user.first_name,
                                                                                            bot_id=Config.BOT_ID, ),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception as e:
                print("An Error occurred when processing inline button[Usage Help]:", e)
                pass
        elif call.data == 'stats':
            from tinydb import TinyDB
            db = TinyDB('database/user/db.json')

            message = "Registered users: {0}".format(len(db))

            ka = telebot.types.InlineKeyboardMarkup(row_width=2)
            kbtn = telebot.types.InlineKeyboardButton("🔄", callback_data='stats')
            kbtn2 = telebot.types.InlineKeyboardButton("🔙", callback_data='back_main_admin')
            ka.row(kbtn, kbtn2)
            bot.edit_message_text(message, call.message.chat.id, call.message.message_id, reply_markup=ka)
        elif call.data == 'back_main_admin':
            kb = telebot.types.InlineKeyboardMarkup()
            kbbtn1 = telebot.types.InlineKeyboardButton("📈 Statistics", callback_data='stats')
            kb.add(kbbtn1)
            bot.edit_message_text("Select one of the options below:", call.message.chat.id, call.message.message_id, reply_markup=kb)


@bot.inline_handler(lambda query: True)  # useless?
def query_text(inline_query):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kbtn1 = types.InlineKeyboardButton("📢My Channel!", url='telegram.me/emaproject')
    kbtn2 = types.InlineKeyboardButton("👁‍🗨@HαlksNET", url='telegram.me/halksnet')
    kb.row(kbtn1, kbtn2)
    r = types.InlineQueryResultArticle('1', 'Inline Search is disabled for maintenance.',
                                       types.InputTextMessageContent(
                                           'Inline search is disabled for maintenance. It will be working soon.'),
                                       reply_markup=kb)
    bot.answer_inline_query(inline_query.id, [r])
"""
    print(inline_query.from_user.first_name + ":" + inline_query.query)

    try:
        load = Img.Query(inline_query.query)
        print(load)
        if load is not None:
            try:
                id = load[0]
                picture = load[8]
                big_picture = load[7]
                if big_picture is None:
                    big_picture = load[8]

                preview_url = load[11]
                try:
                    while True:
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        button = telebot.types.InlineKeyboardButton("💾 Download", url=big_picture)
                        keyboard.add(button)
                        r = types.InlineQueryResultPhoto(str(id), picture, preview_url, reply_markup=keyboard)

                        bot.answer_inline_query(inline_query.id, [r])
                except:
                    pass
            except Exception:
                raise Exception("Error Here.")

        else:
            try:
                input = 'Nobody here but chickens!'
                a = types.InlineQueryResultArticle('1', 'Nobody here but chickens!', input)
                bot.answer_inline_query(inline_query.id, a)
            except Exception:
                raise Exception


    except Exception:
        raise Exception
    time.sleep(1)


    import requests
    import random
    from API.Img import Requests, Posts
    from API import acc_setup as acc
    l = Requests(username=acc.username, password_hash=acc.password_hash,site_name='yandere',
                 api_name='posts_list', param='search')
    site = '{site_url}{api_name}{login}{password}{param}{tags}{limit}'.format(site_url=l.site_url, api_name=l.api_name,
                                                                              login=l.username, password=l.password_hash,
                                                                              param=l.param, tags=inline_query.text,
                                                                              limit=Img.PARAMS['tag_limit'])
    req = requests.get(site)
    ret = req.json()
    quantity = len(ret)
    if quantity == 0:
        r = types.InlineQueryResultArticle('1','Nobody here but chickens!', input_message_content=None)
    else:
        rnum = random.sample(range(0, quantity), 1)
        num = rnum[0]

        id = ret[num]["id"]
        tags = ret[num]["tags"]
        creator_id = ret[num]["creator_id"]
        author = ret[num]["author"]
        source = ret[num]["source"]
        score = ret[num]["score"]
        md5 = ret[num]["md5"]
        file_url = ret[num]["file_url"]
        sample_url = ret[num]["sample_url"]
        width = ret[num]["width"]
        height = ret[num]["height"]
        sample_width = ret[num]["sample_width"]
        sample_height = ret[num]["sample_height"]

        if width and height is None:
            width = sample_width
            height = sample_height
        else:
            pass

        data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height,
                     sample_width, sample_height)

    list = []
"""

"""
@bot.message_handler(func=lambda message: True)  # Handling keyboard buttons
def keyboard(m):

    text = m.text

    if text == "1. Test":
        bot.reply_to(m, en.keyboard['Test'].format(name=m.from_user.first_name), parse_mode='markdown')
    elif text == "2. Test":
        bot.reply_to(m, en.keyboard['Test2'].format(name=m.from_user.first_name), parse_mode='markdown')
    #bot.send_chat_action(cid, 'typing')
    #text == re.search(BotLangEN.msg['Hi'], m.text)

    #if text:
        #bot.send_message(cid, "Hey!")
    #else:
        #if not text:
            #bot.send_message(cid, "Damn :/")
"""


def main_loop():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Exception occurred:", e)
            time.sleep(3)
            main_loop()
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
