# -*- -*-
# _||_ Code Test number 15 _||_
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
# import random

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


bot = telebot.TeleBot(TOKEN, threaded=False)  # register bot token
bot.set_update_listener(listener)  # register listener

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])  # triggers the message for /start command
def send_welcome(m):
    cid = m.chat.id
    match = user_search(str(m.chat.id))

    dp_link = deep_link(m.text)
    if dp_link:
        try:
            lang = match['language']
            bot.send_message(cid, Lang.Lang[lang]['CommandText']['{0}'.format(dp_link)].format(bot_id=Config.BOT_ID),
                             parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print("An Error occurred when processing command /start {0}:".format(dp_link), e)
            pass

    else:

        if not match:
            try:
                ky = types.ReplyKeyboardRemove(selective=False)
                new_user(str(m.from_user.username), str(m.chat.id), 'English', 'Yes', 'Yes')
                bot.reply_to(m, Lang.Lang['English']['CommandText']['start'].format(name=m.from_user.first_name,
                                                                                    bot_name=Config.BOT_NAME),
                             parse_mode='markdown', reply_markup=ky)
            except Exception as e:
                raise Exception(e)
                pass
        else:
            try:
                lang = match['language']
                ky = types.ReplyKeyboardRemove(selective=False)
                bot.reply_to(m, Lang.Lang[lang]['CommandText']['start_reg'].format(name=m.from_user.first_name),
                             parse_mode='markdown', reply_markup=ky)
            except Exception as e:
                print("An error occurred when processing the start_reg:", e)
                pass


@bot.message_handler(commands=['help'])
def send_help(m):
    match = user_search(str(m.chat.id))
    lang = match['language']

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


@bot.message_handler(commands=['about'])
def send_about(m):
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


@bot.message_handler(commands=['admin'])
def admin(m):
    cid = str(m.chat.id)
    master = str(Config.MASTER_ID)

    def send_to_master():
        kb = telebot.types.InlineKeyboardMarkup()
        kbbtn1 = telebot.types.InlineKeyboardButton("📈 Statistics", callback_data='stats')
        kb.add(kbbtn1)
        bot.reply_to(m, "Select one of the options below:", reply_markup=kb)

    send_to_master() if master == cid else bot.reply_to(m, 'Who are you?')


@bot.message_handler(commands=['settings', 'config', 'configurate'])
@bot.message_handler(func=lambda m: m.text == '⚙ Settings')
def settings(m):
    match = user_search(str(m.chat.id))

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


@bot.message_handler(commands=['lang', 'language', 'lang_prefs'])
@bot.message_handler(func=lambda m: m.text in ['🌐 Language', '🌐 Idioma', '🌐 Lenguaje', '🌐 Sprache', '🌐 Язык', '🌐 Lingua'])
def lang(m):
    cid = m.chat.id
    match = user_search(str(cid))
    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']

        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        kbtn1 = types.KeyboardButton("🇧🇷 Português")
        kbtn2 = types.KeyboardButton("🇺🇸 English")
        kbtn3 = types.KeyboardButton("🇪🇸 Español")
        kbtn4 = types.KeyboardButton("🇮🇪 Italiano")
        kbtn5 = types.KeyboardButton("🇷🇺 русский")
        kbtn6 = types.KeyboardButton("🇩🇪 Deutsche")
        kb.add(kbtn2, kbtn1)
        kb.row(kbtn3, kbtn4)
        kb.row(kbtn5, kbtn6)
        try:
            msg = bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['Lang_pref'],
                               parse_mode='markdown', reply_markup=kb)
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
    cid = m.chat.id
    match = user_search(str(cid))
    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        opt = match['notif']
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kbtn1 = types.KeyboardButton("⭕️")
        kbtn2 = types.KeyboardButton("❌")
        if opt == 'Yes':
            btn = kbtn1
        else:
            btn = kbtn2
        kb.add(btn)
        try:
            msg = bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['notif_pref'],
                               parse_mode='markdown', reply_markup=kb)
            bot.register_next_step_handler(msg, chosen_notif)
        except Exception as e:
            print("An error occurred when processing 'Notification Selecto':", e)
            pass


def chosen_notif(m):
    cid = m.chat.id
    user = Query()
    text = m.text
    try:
        if text == "⭕️":
            db.update({'notif': 'No'}, user.id == str(cid))
            msg = "Disabled!"

        elif text == "❌":
            db.update({'notif': 'Yes'}, user.id == str(cid))
            msg = "Enabled!"

        k = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(m, msg, reply_markup=k)
    except Exception as e:
        bot.reply_to(m, 'Ops, something went wrong. Please try again with /notif')
        print("An error occurred when processing 'notif_prefs':", e)
        pass


@bot.message_handler(commands=['ping'])
def pong(m):
    bot.reply_to(m, 'Pong!')


@bot.message_handler(commands=['commands'])
def send_commands(m):
    match = user_search(str(m.chat.id))

    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        try:
            bot.reply_to(m, Lang.Lang[lang]['CommandText']['commands'].format(bot_id=Config.BOT_ID),
                         parse_mode='markdown', disable_web_page_preview=True)
        except Exception as e:
            print("An error occurred when processing /commands:", e)
            pass


@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    match = user_search(str(m.chat.id))

    if not match:
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
@bot.message_handler(commands=['anime', 'ecchi', 'hentai', 'loli', 'yuri'])
def send_media(m):
    cid = m.chat.id
    load_media = m.text.replace("/", "")
    try:
        bot.send_chat_action(cid, 'upload_photo')

        load = Img.post(load_media)

        picture = load['file_url']

        id = load['id']

        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        button = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)
        button2 = telebot.types.InlineKeyboardButton(text="➕ More", callback_data=load_media)
        button3 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))

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

"""
@bot.message_handler(commands=['tag', 'tags'])
def send_tag(m):
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


@bot.message_handler(commands=['id', 'search_id'])
def send_id_query(m):
    cid = m.chat.id
    dp_link = deep_link(m.text)
    if dp_link is None:
        bot.reply_to(m, "Usage:\n `/id [num]` - the num is any number from `1` to `3284774`.")

    try:
        bot.send_chat_action(cid, 'upload_photo')

        load = Img.search_query("id:{0}".format(dp_link))
        picture = load[0]['file_url']

        id = load[0]['id']

        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)
        button3 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))

        try:
            keyboard.add(button)
            keyboard.add(button3)

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
@bot.callback_query_handler(func=lambda call: call.data in load_type)
def media_callback(call):
    if call.message:  # Processes only buttons from messages
        if call.data:
            try:
                bot.send_chat_action(call.message.chat.id, 'upload_photo')

                load = Img.post(call.data)

                picture = load['file_url']

                id = load['id']

                keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                button = telebot.types.InlineKeyboardButton(text="💾 Download", url=picture)
                button2 = telebot.types.InlineKeyboardButton(text="➕ More", callback_data=call.data)
                button3 = telebot.types.InlineKeyboardButton(text="🔘 Share", switch_inline_query="id:{0}".format(id))

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
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=call.data)
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                             parse_mode='markdown', reply_markup=retry_keyboard)
                print("An Error occurred when loading '{0}' dict:".format(call.data), e)
                pass


@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    """
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
    text = inline_query.query
    offset = inline_query.offset
    if offset == '':
        off_set = 0
    else:
        off_set = int(offset)

    try:
        if off_set == 0:
            f = 0
        else:
            f = off_set / 50

        load = Img.search_query(text, pid=int(f))
        nload = len(load)
        if nload == 0:
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
        cache_list = []
        if text.startswith("id:"):
            file = load[0]['file_url']
            id = load[0]['id']
            dirc = load[0]['directory']
            hash = load[0]['hash']
            thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)

            tags = load[0]["tags"].split()
            tags1 = tags[0]
            tags2 = tags[1]
            tags3 = tags[2]

            if file.endswith('.jpg' or '.png' or '.jpeg' or '.bmp'):
                kb = types.InlineKeyboardMarkup(row_width=2)
                kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
                kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                 switch_inline_query_current_chat="{0} {1} {2}".format(tags1,
                                                                                                       tags2,
                                                                                                       tags3))
                kb.row(kb1, kb2)
                r = types.InlineQueryResultPhoto('1', file, thumb, caption='🔖id: {id}\n'.format(id=id),
                                                 reply_markup=kb)
                cache_list.append(r)

            elif file.endswith('.gif'):
                kb = types.InlineKeyboardMarkup(row_width=2)
                kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
                kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                 switch_inline_query_current_chat="{0} {1} {2}".format(tags1,
                                                                                                       tags2,
                                                                                                       tags3))
                kb.row(kb1, kb2)
                r = types.InlineQueryResultGif('1', file, file, caption='🔖id: {id}\n'.format(id=id),
                                               reply_markup=kb)
                cache_list.append(r)

        else:
            for i in range(nload):
                file = load[i]['file_url']
                id = load[i]['id']
                dirc = load[i]['directory']
                hash = load[i]['hash']
                thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)
                if file.endswith('.jpg' or '.png' or '.jpeg' or '.bmp'):
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
                    kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                     switch_inline_query_current_chat=text)
                    kb.row(kb1, kb2)
                    r = types.InlineQueryResultPhoto(str(i), file, thumb,
                                                     caption='🔖id: {id}\n'.format(id=id),
                                                     reply_markup=kb)
                    cache_list.append(r)

                elif file.endswith('.gif'):
                    kb = types.InlineKeyboardMarkup(row_width=2)
                    kb1 = types.InlineKeyboardButton(text="💾 Download", url=file)
                    kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                     switch_inline_query_current_chat=text)
                    kb.row(kb1, kb2)
                    r = types.InlineQueryResultGif(str(i), file, file, caption='🔖id: {id}\n'.format(id=id),
                                                   reply_markup=kb)
                    cache_list.append(r)
                if load[i] is None:
                    break
        b = 50 + off_set
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
        print("Error here:", e)
        pass
# ====================  End of Media Handling  ====================


@bot.callback_query_handler(func=lambda call: True)
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


@bot.message_handler()
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
