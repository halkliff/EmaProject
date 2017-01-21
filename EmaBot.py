# _||_ Code Test number 18 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
from API import Img
from language import Lang
import Config
import os
import random

# ========== Start of user database funcs ==========
from tinydb import TinyDB, Query  # database module

db = TinyDB('database/user/db.json')  # this is the path of the user database


def new_user(from_user_username, from_user_id, from_user_language, from_user_nsfw_choice, from_user_notif_choice):
    # Function to insert user on database. It must fill all the four arguments, or things could go bad on the bot
    db.insert({'id': from_user_id,
               'username': from_user_username,
               'language': from_user_language,
               'nsfw': from_user_nsfw_choice,
               'notif': from_user_notif_choice})


def user_search(from_user_id):
    # Func to search user on database. Returns the dict if the user exists, and None if doesn't match
    # with anything. If the dict is empty, use new_user() func to register the user in the database.
    user = Query()
    a = db.get(user.id == from_user_id)
    if a is not None:
        return a
    else:
        return None

# ========== End of user database funcs ==========


# Deep linking function
def deep_link(text):
    return text.split()[1] if len(text.split()) > 1 else None


# Bot Token taken by @BotFather
TOKEN = Config.TOKEN


# Listener to see when new messages arrives
def listener(messages):

    # When new messages arrive TeleBot will call this function.

    for m in messages:
        if m.content_type == 'text':
            # Print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        # print(str(m))


bot = telebot.AsyncTeleBot(TOKEN, skip_pending=True)  # register bot token
bot.set_update_listener(listener)  # register listener


logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])  # triggers the message for /start command
def send_welcome(m):
    cid = m.chat.id  # Chat unique Identifier
    match = user_search(str(cid))  # Check user database to see if the user exists

    dp_link = deep_link(m.text)
    if dp_link:  # if /start has a parameter
        try:
            lang = match['language']  # If the user exists, gets it's desired language

            bot.send_message(cid, Lang.Lang[lang]['CommandText']['{0}'.format(dp_link)].format(bot_id=Config.BOT_ID),
                             parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
            print("An Error occurred when processing command /start {0}:".format(dp_link), e)
            pass

    else:

        if not match:  # If user couldn't be found in the database
            try:
                ky = types.ReplyKeyboardRemove(selective=False)  # Hides any previous keyboard, if there is

                #  Adds the user in database
                new_user(str(m.from_user.username), str(cid), 'English', 'Yes', 'Yes')

                bot.reply_to(m, Lang.Lang['English']['CommandText']['start'].format(name=m.from_user.first_name,
                                                                                    bot_name=Config.BOT_NAME),
                             parse_mode='markdown', reply_markup=ky)
            except Exception as e:
                raise Exception(e)
                pass
        else:
            try:
                lang = match['language']  # If the user exists, gets it's desired language

                ky = types.ReplyKeyboardRemove(selective=False)  # Hides any previous keyboard, if there is

                bot.reply_to(m, Lang.Lang[lang]['CommandText']['start_reg'].format(name=m.from_user.first_name),
                             parse_mode='markdown', reply_markup=ky)
            except Exception as e:
                print("An error occurred when processing the start_reg:", e)
                pass


@bot.message_handler(commands=['help'])  # sends the help message with buttons
def send_help(m):
    cid = m.chat.id
    match = user_search(str(cid))  # Check user database to see if the user exists

    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:

        lang = match['language']  # If the user exists, gets it's desired language

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


@bot.message_handler(commands=['about'])  # sends an message with info about the bot
def send_about(m):                        # It is interesting to change it to your own info
    msg = """Emα Project
Emα is your personal Eastern Media Assistant, and can help you
fetching content you like from the most famous websites.
*Github repo:* [Emα Project](https://github.com/halkliff/EmaProject)
*Bot Version:* `0.9.3-Beta7`
*API Version:* `2.3.1`


Created, programmed and designed by @Mrhalk
Supported by @DanialNoori94

        *POWERED BY:*
         👁‍🗨_@Hαlks_*NET*
    _Eastern Media Network_
        t.me/HalksNET
"""
    bot.reply_to(m, msg, parse_mode='markdown')


@bot.message_handler(commands=['admin'])  # Admin command, for Statistics, and in the future, for broadacsting
def admin(m):
    cid = str(m.chat.id)  # Chat unique identifier
    master = str(Config.MASTER_ID)  # The bot owner unique identifier

    def send_to_master():
        kb = telebot.types.InlineKeyboardMarkup()
        kbbtn1 = telebot.types.InlineKeyboardButton("📈 Statistics", callback_data='stats')
        kb.add(kbbtn1)
        bot.reply_to(m, "Select one of the options below:", reply_markup=kb)

    send_to_master() if master == cid else bot.reply_to(m, 'Who are you?')  # Sends the message if, and only if,
                                                                            # The user is the owner

@bot.message_handler(commands=['settings', 'config'])  # command triggers for the settings
@bot.message_handler(func=lambda m: m.text == '⚙ Settings')  # Not used yet
def settings(m):
    cid = m.chat.id
    match = user_search(str(cid))

    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        try:
            menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn1 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['lang'])
            btn2 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['notif'])
            # btn3 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['prefs'])
            menu.add(btn1)
            menu.add(btn2)


            bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['set_opt'], reply_markup=menu)
        except Exception as e:
            print("An error occurred when processing /settings:", e)


langs = ['🌐 Language', '🌐 Idioma', '🌐 Lenguaje', '🌐 Sprache', '🌐 Язык', '🌐 Lingua']
@bot.message_handler(commands=['lang', 'language', 'lang_prefs'])  # command triggers for the language selector
@bot.message_handler(func=lambda m: m.text in langs)  # If the text matches the language selectors
def lang(m):
    cid = m.chat.id  # Chat unique Identifier
    match = user_search(str(cid))  # Check user database to see if the user exists
    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']

        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        kbtn1 = types.KeyboardButton("🇧🇷 Português")
        kbtn2 = types.KeyboardButton("🇺🇸 English")
        kbtn3 = types.KeyboardButton("🇪🇸 Español")
        kbtn4 = types.KeyboardButton("🇮🇹 Italiano")
        kbtn5 = types.KeyboardButton("🇷🇺 русский")
        kbtn6 = types.KeyboardButton("🇩🇪 Deutsche")
        kb.add(kbtn2, kbtn1)
        kb.row(kbtn3, kbtn4)
        kb.row(kbtn5, kbtn6)
        try:
            bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['Lang_pref'],
                               parse_mode='markdown', reply_markup=kb)
            #bot.register_next_step_handler(msg, chosen_lang)  # sends the msg, and register the 'chosen_lang' func
        except Exception as e:                                # to be handled next
            print("An error occurred when processing 'Language Selector':", e)
            pass

select_langs = ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español", "🇮🇹 Italiano", "🇷🇺 русский", "🇩🇪 Deutsche"]
@bot.message_handler(func=lambda m: m.text in select_langs)
def chosen_lang(m):
    cid = m.from_user.id  # Chat unique identifier
    user = Query()  # Search the database
    text = m.text.split()  # Breaks the text, so it returns a list
    try:
        db.update({'language': text[1]}, user.id == str(cid))  # Updates the database with the second item in the list

        k = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(m, Lang.Lang[text[1]]['keyboard']['messages']['Chosen_lang'],
                     parse_mode='markdown', reply_markup=k)
    except Exception as e:
        bot.reply_to(m, 'Ops, something went wrong. Please try again with /language')
        print("An error occurred when processing 'new_user_lang_register':", e)
        pass


ntf_string = ['🔔 Notifications', '🔔 Notificações', '🔔 Notificaciones',
              '🔔 Benachrichtigungen', '🔔 Оповещения', '🔔 Notifiche']
@bot.message_handler(commands=['notif', 'notifications',])
@bot.message_handler(func=lambda m: m.text in ntf_string)
def send_notif(m):
    cid = m.chat.id  # Chat unique identifier
    match = user_search(str(cid))  # Check user database to see if the user exists
    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']  # User language
        opt = match['notif']  # User notification choice 'yes/no"
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kbtn1 = types.KeyboardButton("⭕️")
        kbtn2 = types.KeyboardButton("❌")
        if opt == 'Yes':  # If the user already has notifications on, it turns off
            btn = kbtn1
        else:  # If the user has notifications off, it turns on
            btn = kbtn2
        kb.add(btn)
        try:
            bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['notif_pref'],
                               parse_mode='markdown', reply_markup=kb)
            #bot.register_next_step_handler(msg, chosen_notif)  # sends the msg, and register the 'chosen_notif' func
        except Exception as e:                                 # to be handled next
            print("An error occurred when processing 'Notification Selector':", e)
            pass


ntf_opt = ["⭕️", "❌"]
@bot.message_handler(func=lambda m: m.text in ntf_opt)
def chosen_notif(m):
    cid = m.chat.id  # Chat unique identifier
    user = Query()  # Search the database
    text = m.text  # gets the emoji text to handle in the database
    try:
        if text == "⭕️":
            db.update({'notif': 'No'}, user.id == str(cid))  # The notifications were on, so now they'll be disabled
            msg = "Disabled!"

        elif text == "❌":
            db.update({'notif': 'Yes'}, user.id == str(cid))  # The notifications were off, so now they'll be enabled
            msg = "Enabled!"

        k = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(m, msg, reply_markup=k)
    except Exception as e:
        bot.reply_to(m, 'Ops, something went wrong. Please try again with /notif')
        print("An error occurred when processing 'notif_prefs':", e)
        pass


@bot.message_handler(commands=['ping'])  # This is just to check if the bot is online. Nothing special
def pong(m):
    bot.reply_to(m, 'Pong!')


@bot.message_handler(commands=['commands'])  # Commands list
def send_commands(m):
    cid = m.chat.id
    match = user_search(str(cid))  # Check user database to see if the user exists

    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        try:
            bot.reply_to(m, Lang.Lang[lang]['CommandText']['commands'].format(bot_id=Config.BOT_ID),
                         parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print("An error occurred when processing /commands:", e)
            pass


@bot.message_handler(commands=['inline_help']) # Sends the Inline help
def send_inline_help(m):
    cid = m.chat.id
    match = user_search(str(cid))  # Check user database to see if the user exists

    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        try:
            bot.reply_to(m,
                         Lang.Lang[lang]['CommandText']['inline_help'].format(bot_id=Config.BOT_ID),
                         parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print("An Error occurred when processing command /inline_help:", e)
            pass


# ==================== Start of Media Handling ====================
@bot.message_handler(commands=['anime', 'ecchi', 'hentai', 'loli', 'yuri'])  #All the available media commands
def send_media(m):
    cid = m.chat.id  # Chat unique identifier
    load_media = m.text.replace("/", "")  # Removes the "/" from the command, so it gets as a normal word
    try:
        bot.send_chat_action(cid, 'upload_photo')  # Sends "uploading photo" chat action

        load = Img.post(load_media)  # Loads the json object with the query

        picture = load['file_url']  # The picture url

        id = load['id']  # The picture unique identifier, on the server

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        button = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)  # Download button
        button2 = telebot.types.InlineKeyboardButton(text="➕ More", callback_data=load_media)  # load more
        button3 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))  # Share

        try:
            keyboard.row(button, button3)
            keyboard.add(button2)

            bot.send_photo(cid, picture, caption='🔖id: {id}\n'.format(id=id), reply_markup=keyboard)
        except Exception as e:
            retry_keyboard = telebot.types.InlineKeyboardMarkup()
            retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=load_media)
            retry_keyboard.add(retry_button)

            bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                         parse_mode='markdown', reply_markup=retry_keyboard)
            print("An error Occurred in /{0}:".format(load_media), e)
            pass
    except Exception as e:
        retry_keyboard = telebot.types.InlineKeyboardMarkup()
        retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=load_media)
        retry_keyboard.add(retry_button)

        bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                     parse_mode='markdown', reply_markup=retry_keyboard)
        print("An Error occurred when loading '{0}' dict:".format(load_media), e)
        pass


@bot.message_handler(commands=['tag', 'tags'])
def send_tag(m):
    bot.reply_to(m, "This command is not set to work now. See /commands")
    """
    cid = m.chat.id
    text = m.text.replace("/tags", "")
    try:
        load_tags = Img.search_query(text)

        n = load_tags
        rload = random.choice(range(0, len(n)))

        picture = load_tags[rload]['file_url']
        id = load_tags[rload]['id']

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="💾 Download", url=picture)
        # button2 = telebot.types.InlineKeyboardButton(text="More", callback_data=load_media)
        try:
            keyboard.add(button1)

            bot.send_chat_action(cid, 'upload_photo')
            bot.send_photo(cid, picture, caption='🔖id: {id}\n'.format(id=id), reply_markup=keyboard)
        except Exception as e:
            bot.send_message(cid, "Wasn't able to proceed your request.")
            print("An error Occurred in /tags:", e)
            pass
    except Exception as e:
        bot.reply_to(m, 'Wooops, something went wrong. Try again!')
        print("An error occurred when processing /tags:", e)
        pass
"""


@bot.message_handler(commands=['id', 'search_id'])  # Searches any server id
def send_id_query(m):
    cid = m.chat.id  # Chat unique identifier
    dp_link = deep_link(m.text)
    if dp_link is None:  # if /id has not a parameter
        bot.reply_to(m, "Usage:\n `/id [num]` - the num is any number from `1` to `3284774`.", parse_mode='markdown')
    else:

        try:
            bot.send_chat_action(cid, 'upload_photo')  # Sends "uploading photo" chat action

            load = Img.search_query("id:{0}".format(dp_link))  # Loads the json object with the query
            picture = load[0]['file_url']  # The picture url

            id = load[0]['id']  # The picture unique identifier, on the server

            keyboard = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)  # Download button
            btn2 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))  # Share

            try:
                keyboard.add(btn)
                keyboard.add(btn2)

                bot.send_photo(cid, picture, caption='🔖id: {id}\n'.format(id=id), reply_markup=keyboard)
            except Exception as e:
                bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.",
                             parse_mode='markdown')
                print("An error Occurred in /id {0}:".format(dp_link), e)
                pass

        except Exception as e:
            bot.reply_to(m, "Sorry!\n`An unexpected error occurred when processing your request`.",
                         parse_mode='markdown')
            print("An Error occurred when loading 'id' dict:", e)
            pass


load_type = ['anime', 'ecchi', 'loli', 'hentai', 'yuri']
@bot.callback_query_handler(func=lambda call: call.data in load_type)  # Whenever the user taps the "more" button,
def media_callback(call):                                              # It triggers this function
    if call.message:  # Processes only buttons from messages
        if call.data:  # If there's any data callback
            try:
                bot.send_chat_action(call.message.chat.id, 'upload_photo')  # Sends "uploading photo" chat action

                load = Img.post(call.data)  # Loads the json object with the query

                picture = load['file_url']  # The picture url

                id = load['id']  # The picture unique identifier, on the server

                keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                button = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)  # Download button
                button2 = telebot.types.InlineKeyboardButton(text="➕ More", callback_data=call.data)  # more
                button3 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))
                #Share
                try:
                    keyboard.row(button, button3)
                    keyboard.add(button2)

                    bot.send_photo(call.message.chat.id, picture, caption='🔖id: {id}\n'.format(id=id),
                                   reply_markup=keyboard)
                except Exception as e:
                    retry_keyboard = telebot.types.InlineKeyboardMarkup()
                    retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=call.data)
                    retry_keyboard.add(retry_button)

                    bot.reply_to(call.message.chat.id,
                                 "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                                 parse_mode='markdown', reply_markup=retry_keyboard)
                    print("An Error occurred in 'more {0}':".format(call.data), e)
                    pass
            except Exception as e:
                print("An Error occurred when loading '{0}' dict:".format(call.data), e)
                pass


@bot.inline_handler(lambda query: True)  # Inline mode. YAY!
def query_text(inline_query):
    text = inline_query.query  # The text input by the user, where @bot_name [text] is this text
    offset = inline_query.offset  # Checks if there is any offset by the query
    if offset == '':  # If there's no offset
        off_set = 0
    else:  # If there's a offset
        off_set = int(offset)

    try:
        if off_set == 0:        # All of this is just to work with the API
            f = 0               # There's nothing really to explain, as it
        else:                   # is complicated to me to do so.
            f = off_set

        load = Img.search_query(text, pid=int(f))  # Loads a json object with the query
        nload = len(load)  # calculates how much data there's in load
        if nload == 0:  # if there's no data in 'load'
            msg = """
                    _Looks like you tried some tag combinations that didn't work properly..._
                    _But don't worry! just try up another tag combination!_
                    """
            key = types.InlineKeyboardMarkup(row_width=2)
            k1 = types.InlineKeyboardButton("📢My Channel!", url='t.me/emaproject')
            k2 = types.InlineKeyboardButton("👁‍🗨@HαlksNET", url='t.me/halksnet')
            key.row(k1, k2)
            fgw = types.InlineQueryResultArticle('1',
                                                'Nothing here but my cookies!',
                                                 types.InputTextMessageContent(msg, parse_mode='markdown'),
                                                 reply_markup=key,
                                                 description='Looks like you tried some tag combinations that...')
            bot.answer_inline_query(inline_query.id, [fgw])

        if text.startswith("id:"):  # If the query starts with 'id:', which means it came from a "Share" instance
            result = []

            file = load[0]['file_url']  # File url
            id = load[0]['id']  # File unique identifier in the server
            dirc = load[0]['directory']  # Directory where it is stored in the server
            hash = load[0]['hash']  # The hash string provided by the server
            thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)  # A complicated thumbnail
                                                                                               # builder
            tags = load[0]["tags"].split()  # Splits the tags in a list
            tags1 = tags[0]  # These are just
            tags2 = tags[1]  # to load up to
            tags3 = tags[2]  # three tags

            kb = types.InlineKeyboardMarkup(row_width=2)
            kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
            kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                             switch_inline_query_current_chat="{0} {1} {2}".format(tags1,
                                                                                                   tags2,
                                                                                                   tags3))
            kb.row(kb1, kb2)

            if file.endswith('.gif'):  # if the file is a gif
                gif = types.InlineQueryResultGif('1', file, file, caption='🔖id: {id}\n'.format(id=id),
                                               reply_markup=kb)
                result.append(gif)  # inserts the object in the cache database

            else:  # if the file is any type of image
                pic = types.InlineQueryResultPhoto('1', file, thumb, caption='🔖id: {id}\n'.format(id=id),
                                                     reply_markup=kb)
                result.append(pic)  # inserts the object in the cache database

            bot.answer_inline_query(inline_query.id, result, is_personal=True)

        else:  # if it is a normal query
            cache_list = []  # This is the cache database the bot will send
            af = 0

            for i in load:  # this 'for' loop inserts on the 'cache_list' up to 50 objects for the query result
                file = i['file_url']  # file url
                id = i['id']  # File unique identifier in the server
                dirc = i['directory']  # Directory where it is stored in the server
                hash = i['hash']  # The hash string provided by the server
                thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)  # again, the odd
                                                                                                   # thumbnail stuff
                kb = types.InlineKeyboardMarkup(row_width=2)
                kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
                kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                 switch_inline_query_current_chat=text)
                kb.row(kb1, kb2)
                if file.endswith('.gif'):  # if the file is gif
                    gif = types.InlineQueryResultGif(str(int(af)), file, thumb_url=file,
                                                     caption='🔖id: {id}\n'.format(id=id),
                                                     reply_markup=kb)
                    cache_list.append(gif)  # inserts the object in the cache
                else:  # if the file is any type of image
                    pic = types.InlineQueryResultPhoto(str(int(af)), file, thumb_url=thumb,
                                                           caption='🔖id: {id}\n'.format(id=id),
                                                           reply_markup=kb)
                    cache_list.append(pic)  # inserts the object in the cache
                    
                af += 1  # Number of id to be sent to Telegram Server

            b = 1 + off_set  # Complicated stuff, this is for the offset
            bot.answer_inline_query(inline_query.id, cache_list, next_offset=b, cache_time=120,
                                    switch_pm_text="Usage help", switch_pm_parameter="tags")

    except Exception as e:
        msg = """
                _Looks like you tried some tag combinations that didn't work properly..._
                _But don't worry! just try up another tag combination!_
                """
        key = types.InlineKeyboardMarkup(row_width=2)
        k1 = types.InlineKeyboardButton("📢My Channel!", url='t.me/emaproject')
        k2 = types.InlineKeyboardButton("👁‍🗨@HαlksNET", url='t.me/halksnet')
        key.row(k1, k2)
        fgw = types.InlineQueryResultArticle('1', 'Nothing here but my cookies!',
                                             types.InputTextMessageContent(msg, parse_mode='markdown'),
                                             reply_markup=key,
                                             description='Looks like you tried some tag combinations that...')
        bot.answer_inline_query(inline_query.id, [fgw])
        print("An error occurred with the query '{0}':".format(inline_query.query), e)
        pass
# ====================  End of Media Handling  ====================


@bot.callback_query_handler(func=lambda call: True)  # The other inline button calls
def callback_inline(call):
    if call.message:  # Processes only buttons from messages
        if call.data == "commands":
            match = user_search(str(call.message.chat.id))

            if not match:
                bot.reply_to(call.message.chat.id,
                             "Ooops, looks like you're not registered. Please tap /start to register.")
            else:
                lang = match['language']
                try:
                    bot.send_message(call.message.chat.id,
                                     Lang.Lang[lang]['CommandText']['commands'].format(bot_id=Config.BOT_ID),
                                     parse_mode='markdown', disable_web_page_preview=True)
                except Exception as e:
                    print("An error occurred when processing the inline button 'Commands':", e)
                    pass

        elif call.data == "inline_help":
            match = user_search(str(call.message.chat.id))

            if not match:
                bot.reply_to(call.message.chat.id,
                             "Ooops, looks like you're not registered. Please tap /start to register.")
            else:
                lang = match['language']
                try:
                    bot.send_message(call.message.chat.id,
                                     Lang.Lang[lang]['CommandText']['inline_help'].format(bot_id=Config.BOT_ID),
                                     parse_mode='markdown', disable_web_page_preview=True)
                except Exception as e:
                    print("An Error occurred when processing inline button [Inline Help]:", e)
                    pass

        elif call.data == "tags":
            match = user_search(str(call.message.chat.id))

            if not match:
                bot.reply_to(call.message.chat.id,
                             "Ooops, looks like you're not registered. Please tap /start to register.")
            else:
                lang = match['language']
                try:
                    bot.send_message(call.message.chat.id,
                                     Lang.Lang[lang]['CommandText']['tags'].format(bot_id=Config.BOT_ID),
                                     parse_mode='markdown',)
                except Exception as e:
                    print("An Error occurred when processing inline button [Tags]:", e)
                    pass

        elif call.data == "source_id":
            match = user_search(str(call.message.chat.id))

            if not match:
                bot.reply_to(call.message.chat.id,
                             "Ooops, looks like you're not registered. Please tap /start to register.")
            else:
                lang = match['language']
                try:
                    bot.send_message(call.message.chat.id,
                                     Lang.Lang[lang]['CommandText']['source_id'],
                                     parse_mode='markdown',)
                except Exception as e:
                    print("An Error occurred when processing inline button [Source ID]:", e)
                    pass

        elif call.data == "help_use":
            match = user_search(str(call.message.chat.id))

            if not match:
                bot.reply_to(call.message.chat.id,
                             "Ooops, looks like you're not registered. Please tap /start to register.")
            else:
                lang = match['language']
                try:
                    bot.send_message(call.message.chat.id,
                                     Lang.Lang[lang]['CommandText']['help_use'].format(name=call.from_user.first_name,
                                                                                       bot_id=Config.BOT_ID,),
                                     parse_mode='markdown', disable_web_page_preview=True)
                except Exception as e:
                    print("An Error occurred when processing inline button[Usage Help]:", e)
                    pass

        elif call.data == 'stats':
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
            bot.edit_message_text("Select one of the options below:", call.message.chat.id,
                                  call.message.message_id, reply_markup=kb)


@bot.message_handler()  # If the user types anything that is not supported by the bot, like messages or commands
def send_random(m):
    cid = m.chat.id
    msg1 = "Woops, I can't chat yet. Please see /help."
    msg2 = "Sorry, I do not have that command, please see /commands for all my functions."
    if m.text.startswith("/"):
        bot.send_message(cid, msg2, disable_notification=True)
    else:
        dec = ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español", "🇮🇪 Italiano", "🇩🇪 Deutsche", "🇷🇺 русский", "⭕️", "❌"]

        if m.text not in dec:
            bot.send_message(cid, msg1, disable_notification=True)


# ================================================= Loop the polling =================================================
def main_loop():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Exception occurred:", e)
            break
            time.sleep(2)
            os.execv(sys.executable, ['python'] + sys.argv)
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
