# _||_ Code Test number 22 _||_
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
from database import Data

# ================================================== Start of caches ==================================================
broadcast_ids = []
nsfw_ids = []
Data.broadcast_append(broadcast_ids)  # This will bring to the broadcast_ids all ids.
Data.mature_enabled_users(nsfw_ids)  #This will cache users that enabled mature content, for speed purposes

# =================================================== End of caches ===================================================

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

# Deep linking function
def deep_link(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'])  # triggers the message for /start command
def send_welcome(m):
    cid = m.chat.id  # Chat unique Identifier
    match = Data.user_search(str(cid))  # Check user database to see if the user exists

    dp_link = deep_link(m.text)
    if dp_link:  # if /start has a parameter
        if dp_link.startswith("share"):
            splt = dp_link.split('&')
            param = splt[1]
            try:
                msg = u'Your selected file is ready to be shared!\n' \
                      u'Tap the button below, select a chat, and then share\n' \
                      u'your file!'

                keyboard = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton("Share", switch_inline_query=param)
                keyboard.add(button1)

                bot.send_message(cid, msg, reply_markup=keyboard)

            except Exception as e:
                print("An error occurred on inline parameter 'share':", e)
                pass

        else:
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
                Data.new_user(str(m.from_user.username), str(cid), 'English')

                bot.reply_to(m, Lang.Lang['English']['CommandText']['start'].format(name=m.from_user.first_name,
                                                                                    bot_name=Config.BOT_NAME),
                             parse_mode='markdown', reply_markup=ky)
                broadcast_ids.append(str(cid))
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
    match = Data.user_search(str(cid))  # Check user database to see if the user exists

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
*Bot Version:* `0.9.4.3` - [Changelog](https://t.me/EmaProject/27)
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
    match = Data.user_search(str(cid))

    if not match:
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']
        try:
            menu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['lang'])
            btn2 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['notif'])
            btn3 = types.KeyboardButton('⚠️ Preferences')
            btn4 = types.KeyboardButton(Lang.Lang[lang]['keyboard']['buttons']['hide_kb'])
            menu.row(btn1, btn2)
            menu.add(btn3)
            menu.add(btn4)

            bot.reply_to(m, Lang.Lang[lang]['keyboard']['messages']['set_opt'], reply_markup=menu)
        except Exception as e:
            print("An error occurred when processing /settings:", e)


@bot.message_handler(commands=['broadcast'])
def broadcast(m):

    kb = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton("Click here", callback_data='broadcast_test')
    kb.add(kb1)
    for id in broadcast_ids:
        count = 0
        bot.send_message(id, "Broadcast test, please click in the button below if you receive this message.",
                         reply_markup=kb)
        count += 1

        if count >= 20:
            print('sleeping')
            time.sleep(3)
            continue


@bot.callback_query_handler(func= lambda call: call.data == "broadcast_test")
def updt_broadcast(call):
    if call.message:
        if call.data:
            bot.send_message(chat_id=call.message.chat.id, text="Thanks!", reply_to_message_id=call.message.message_id)
            bot.send_message(chat_id=Config.MASTER_ID, text="User confirmed")


langs = ['🌐 Language', '🌐 Idioma', '🌐 Lenguaje', '🌐 Sprache', '🌐 Язык', '🌐 Lingua']
@bot.message_handler(commands=['lang', 'language', 'lang_prefs'])  # command triggers for the language selector
@bot.message_handler(func=lambda m: m.text in langs)  # If the text matches the language selectors
def lang(m):
    cid = m.chat.id  # Chat unique Identifier
    match = Data.user_search(str(cid))  # Check user database to see if the user exists
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
            # bot.register_next_step_handler(msg, chosen_lang)  # sends the msg, and register the 'chosen_lang' func
        except Exception as e:                                # to be handled next
            print("An error occurred when processing 'Language Selector':", e)
            pass

select_langs = ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español", "🇮🇹 Italiano", "🇷🇺 русский", "🇩🇪 Deutsche"]
@bot.message_handler(func=lambda m: m.text in select_langs)
def chosen_lang(m):
    cid = m.from_user.id  # Chat unique identifier
    text = m.text.split()  # Breaks the text, so it returns a list
    try:
        Data.update_user_language(str(cid), text[1])  # Updates the database with the second item in the list

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
    match = Data.user_search(str(cid))  # Check user database to see if the user exists
    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        lang = match['language']  # User language
        opt = match['notif']  # User notification choice 'yes/no'"
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
            # bot.register_next_step_handler(msg, chosen_notif)  # sends the msg, and register the 'chosen_notif' func
        except Exception as e:                                 # to be handled next
            print("An error occurred when processing 'Notification Selector':", e)
            pass


ntf_opt = ["⭕️", "❌"]
@bot.message_handler(func=lambda m: m.text in ntf_opt)
def chosen_notif(m):
    cid = m.chat.id  # Chat unique identifier
    text = m.text
    try:
        Data.toggle_stat_notifications(str(cid))
        if text == "⭕️":
            msg = "Disabled!"
            broadcast_ids.remove(str(cid))

        elif text == "❌":
            msg = "Enabled!"
            broadcast_ids.append(str(cid))

        k = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(m, msg, reply_markup=k)
    except Exception as e:
        bot.reply_to(m, 'Ops, something went wrong. Please try again with /notif')
        print("An error occurred when processing 'notif_prefs':", e)
        pass


@bot.message_handler(commands=['nsfw', 'prefs', 'preferences'])
@bot.message_handler(func=lambda m: m.text == '⚠️ Preferences')
def send_prefs(m):
    cid = m.chat.id  # Chat unique identifier
    match = Data.user_search(str(cid))  # Check user database to see if the user exists
    if not match:  # If user not found in the database
        bot.reply_to(m, "Ooops, looks like you're not registered. Please tap /start to register.")
    else:
        pref = match['nsfw']  # User notification choice 'yes/no'"
        kb = types.InlineKeyboardMarkup()
        kbtn1 = types.InlineKeyboardButton("Tap to enable Mature Content", callback_data="enable_nsfw")
        kbtn2 = types.InlineKeyboardButton("Tap to disable Mature Content", callback_data="disable_nsfw")
        if pref == 'Yes':  # If the user already has notifications on, it turns off
            btn = kbtn1
            msg = "Mature content Preference.\n Your current status is: `Disabled`"
        else:  # If the user has notifications off, it turns on
            btn = kbtn2
            msg = "Mature content Preference.\n Your current status is: `Enabled`"
        kb.add(btn)
        try:
            bot.reply_to(m, msg, parse_mode='markdown', reply_markup=kb)
        except Exception as e:
            print("An error occurred when processing 'Notification Selector':", e)
            pass

pref = ["enable_nsfw", "disable_nsfw"]
@bot.callback_query_handler(func= lambda call: call.data in pref)
def chosen_prefs(call):
    if call.message:
        if call.data:
            cid = call.message.chat.id
            text = call.data

            try:
                Data.toggle_stat_nsfw(str(cid))

                kb = telebot.types.InlineKeyboardMarkup()

                if text == pref[1]:
                    msg = "Disabled mature content."
                    kbtn1 = types.InlineKeyboardButton("Tap to enable Mature Content", callback_data="enable_nsfw")
                    kb.add(kbtn1)
                    nsfw_ids.remove(str(cid))

                elif text == pref[0]:
                    msg = "Enabled mature content."
                    kbtn1 = types.InlineKeyboardButton("Tap to disable Mature Content", callback_data="disable_nsfw")
                    kb.add(kbtn1)
                    nsfw_ids.append(str(cid))

                    alert = "Warning!\n" \
                            "Mature content (+18) is now enabled. If it was not supposed to enable this behavior,\n" \
                            "please use the command /prefs and disable it!"
                    bot.answer_callback_query(call.id, text=alert, show_alert=True)
                bot.edit_message_text(msg, cid, call.message.message_id, reply_markup=kb)

            except Exception as e:
                bot.send_message(cid, 'Ops, something went wrong. Please try again with /prefs')
                print("An error occurred when processing 'nsfw_prefs':", e)
                pass


@bot.message_handler(commands=['ping'])  # This is just to check if the bot is online. Nothing special
def pong(m):
    bot.reply_to(m, 'Pong!')


@bot.message_handler(commands=['commands'])  # Commands list
def send_commands(m):
    cid = m.chat.id
    match = Data.user_search(str(cid))  # Check user database to see if the user exists

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


@bot.message_handler(commands=['inline_help'])  # Sends the Inline help
def send_inline_help(m):
    cid = m.chat.id
    match = Data.user_search(str(cid))  # Check user database to see if the user exists

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


# ============================================== Start of Media Handling ==============================================
cmnd_list = ['anime', 'ecchi', 'hentai', 'loli', 'yuri', 'sweater_dress', 'yaoi', 'animal_ears']
@bot.message_handler(commands=cmnd_list)
def send_media(m):  # All the available media commands
    cid = m.chat.id  # Chat unique identifier
    load_media = m.text.replace("/", "")  # Removes the "/" from the command, so it gets as a normal word
    if load_media is not 'anime' or 'animal_ears':
        if str(cid) not in nsfw_ids:
            msg = "You are trying to use a Not Safe For Work command, but your configuration has\n" \
                  "disabled mature content! To use this command, you should first enable\n" \
                  "mature content view in /preferences."
            bot.send_message(cid, msg)
        else:
            try:
                bot.send_chat_action(cid, 'upload_photo')  # Sends "uploading photo" chat action

                load = Img.post(load_media)  # Loads the json object with the query

                file = load['file_url']  # The picture url

                id = load['id']  # The picture unique identifier, on the server

                dirc = load['directory']

                img = load['image']

                download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
                button = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
                button2 = telebot.types.InlineKeyboardButton(text="➕",
                                                             callback_data=
                                                             load_media + " id={0}".format(id) + ' fav=No')  # load more
                button3 = telebot.types.InlineKeyboardButton(text="🔘", switch_inline_query="id:{0}".format(id))  # Share
                button4 = telebot.types.InlineKeyboardButton(text="⭐️",
                                                             callback_data=
                                                             'favorite_add={id}&media={md}'.format(id=id, md=load_media))
                button5 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

                try:
                    keyboard.row(button, button3, button5, button4)
                    keyboard.add(button2)
                    if file.endswith('.gif'):
                        bot.send_document(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)

                    else:
                        bot.send_photo(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)

                    Data.update_media_processed()
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


@bot.message_handler(commands=['id', 'search_id'])  # Searches any server id
def send_id_query(m):
    cid = m.chat.id  # Chat unique identifier
    dp_link = deep_link(m.text)
    if dp_link is None:  # if /id has not a parameter
        bot.reply_to(m, "Usage:\n `/id [num]` - the num is any number from `1` to `3284774`.", parse_mode='markdown')
    else:

        try:
            bot.send_chat_action(cid, 'upload_document')  # Sends "uploading photo" chat action

            load = Img.search_query("id:{0}".format(dp_link))  # Loads the json object with the query
            file = load[0]['file_url']  # The picture url

            id = load[0]['id']  # The picture unique identifier, on the server

            dirc = load[0]['directory']

            img = load[0]['image']

            download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

            keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
            btn = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
            btn2 = telebot.types.InlineKeyboardButton(text="🔘", switch_inline_query="id:{0}".format(id))  # Share
            btn3 = telebot.types.InlineKeyboardButton(text="⭐️", callback_data='favorite_add={id}'.format(id=id,))
            btn4 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

            try:
                keyboard.add(btn, btn2, btn4, btn3)
                if file.endswith('.gif'):
                    bot.send_document(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)
                    """elif file.endswith('.webm'):  # picture.endswith('.mp4'):
                    bot.send_message(cid, '[🔖]({file})id: {id}\n'.format(id=id, file=file))"""

                else:
                    bot.send_photo(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)

                Data.update_media_processed()
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


load_type = ['anime', 'ecchi', 'loli', 'hentai', 'yuri', 'sweater_dress', 'yaoi', 'animal_ears']
@bot.callback_query_handler(func=lambda call: call.data.split()[0] in load_type)  # Whenever the user taps the "more"
def media_callback(call):                                                         # button, it triggers this function
    if call.message:  # Processes only buttons from messages
        if call.data:  # If there's any data callback
            splt = call.data.split()
            param = splt[0]
            call_id = splt[1].split('=')[1]
            has_favorited = splt[2].split('=')[1]

            cid = call.message.chat.id
            try:
                bot.send_chat_action(call.message.chat.id, 'upload_photo')  # Sends "uploading photo" chat action

                load = Img.post(param)  # Loads the json object with the query

                # file = load['file_url']  # The picture url

                id = load['id']  # The picture unique identifier, on the server

                dirc = load['directory']

                img = load['image']

                download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                button = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
                button2 = telebot.types.InlineKeyboardButton(text="➕",
                                                             callback_data=
                                                             param + " id={0}".format(id) + ' fav=No')  # load more
                button3 = telebot.types.InlineKeyboardButton(text="🔘",
                                                             switch_inline_query="id:{0}".format(id))  # Share
                button4 = telebot.types.InlineKeyboardButton(text="⭐️",
                                                             callback_data=
                                                             'favorite_add={id}&media={md}'.format(id=id, md=param))
                button5 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

                try:
                    keyboard.row(button, button3, button5, button4)
                    keyboard.add(button2)

                    if img.endswith('.gif'):
                        bot.send_document(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)

                    else:
                        bot.send_photo(cid, download_url, caption='🎴ID: {id}\n'.format(id=id), reply_markup=keyboard)

                    Data.update_media_processed()

                except Exception as e:
                    retry_keyboard = telebot.types.InlineKeyboardMarkup()
                    retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=call.data)
                    retry_keyboard.add(retry_button)

                    bot.send_message(cid,
                                     "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                                     parse_mode='markdown', reply_markup=retry_keyboard)
                    print("An Error occurred in 'more {0}':".format(call.data), e)
                    pass

                try:
                    load = Img.search_query("id:{0}".format(call_id))  # Loads the json object with the query

                    dirc = load[0]['directory']

                    img = load[0]['image']

                    download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                    button = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
                    button3 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                 switch_inline_query='id:{0}'.format(call_id))  # Share
                    button41 = telebot.types.InlineKeyboardButton(text="⭐️",
                                                                  callback_data='favorite_add={id}'.format(id=call_id))
                    button42 = telebot.types.InlineKeyboardButton(text="🌟",
                                                                  callback_data='favorite_del={id}'.format(id=call_id))
                    button5 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=call_id))

                    if has_favorited == "Yes":
                        keyboard.row(button, button3, button5, button42)

                    else:
                        keyboard.row(button, button3, button5, button41)

                    bot.edit_message_reply_markup(cid, call.message.message_id, reply_markup=keyboard)

                except Exception as e:
                    msg = "Woops, I couldn't update your buttons, but don't worry! Your favorite was saved."
                    bot.answer_callback_query(call.id, text=msg, show_alert=True)
                    print("An Error occurred when tried to update the fav_btn:", e)
                    pass

            except Exception as e:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data=call.data)
                retry_keyboard.add(retry_button)

                bot.send_message(cid,
                                 "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?",
                                 parse_mode='markdown', reply_markup=retry_keyboard)
                print("An Error occurred when loading '{0}' dict:".format(call.data), e)
                pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("info"))
def answer_info(call):
    if call.message:
        if call.data:
            bot.send_chat_action(call.message.chat.id, 'typing')
            splt = call.data.split("=")
            id = splt[1]
            try:
                load = Img.search_query("id:{0}".format(id))

                width = load[0]["width"]
                height = load[0]["height"]
                id = load[0]["id"]
                view_webpage = 'http://gelbooru.com/index.php?page=post&s=view&id={id}'.format(id=id)
                tags = load[0]["tags"]
                owner = load[0]["owner"]

                rt = load[0]["rating"]
                if rt == "s":
                    rating = "Safe"
                elif rt == "q":
                    rating = "Questionable"

                elif rt == "e":
                    rating = "Explicit"

                parent_id = load[0]["parent_id"]

                if parent_id is None:
                    parent_answer = "No"

                else:
                    parent_answer = "_Yes, Parent ID:_ [{0}](http://gelbooru.com/index.php?page=post&s=view&id={0})".format(
                        parent_id)

                msg = Lang.msg['msg']
                true_msg = msg.format(id=id, parent_post=parent_answer, W=width, H=height,
                                      Owner=owner, rating=rating, tags=tags)

                kb = telebot.types.InlineKeyboardMarkup()
                kb1 = telebot.types.InlineKeyboardButton(text="View Web Page", url=view_webpage)
                try:
                    kb.add(kb1)
                    bot.send_message(call.message.chat.id, true_msg, parse_mode='markdown',
                                     disable_web_page_preview=True, reply_to_message_id=call.message.message_id,
                                     reply_markup=kb)
                except Exception as e:
                    print("Error here bro:", e)

            except Exception as e:
                print("An error occurred when tried to send info about file id {0}:".format(id), e)
                pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("favorite"))
def favs_handler(call):
    if call.message:
        cid = call.message.chat.id

        splt = call.data.split('&')
        func = splt[0].split('=')[0]  # May be 'favorite_add=' or 'favorite_del='
        id = splt[0].split('=')[1]  # The file id
        load_media = splt[1].split('=')[1] if len(splt) >= 2 else ""
        match = Data.search_favorites(str(cid))['favorites']

        if func == 'favorite_add':
            try:
                if id in match:
                    bot.answer_callback_query(call.id, text="This file is already on favorites.")
                else:
                    Data.add_favorites(str(cid), id)
                    bot.answer_callback_query(call.id, text="Added to favorites")

                try:
                    load = Img.search_query("id:{0}".format(id))  # Loads the json object with the query

                    dirc = load[0]['directory']

                    img = load[0]['image']

                    download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                    button = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
                    button2 = telebot.types.InlineKeyboardButton(text="➕",
                                                                 callback_data=
                                                                 load_media + " id={0}".format(id) + ' fav=Yes')  # load more
                    button3 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                 switch_inline_query='id:{0}'.format(id))  # Share
                    button41 = telebot.types.InlineKeyboardButton(text="🌟",
                                                                  callback_data='favorite_del={id}'.format(id=id))
                    button42 = telebot.types.InlineKeyboardButton(text="🌟",
                                                                  callback_data='favorite_del={id}&media={md}'.format(
                                                                      id=id,
                                                                      md=load_media))
                    button5 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

                    if load_media.startswith("True"):

                        redo_btn = telebot.types.InlineKeyboardButton(text="❌",
                                                                      callback_data=
                                                                      "favorite_del={id}&fav_command=True".format(
                                                                          id=id))

                        button2 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                     switch_inline_query="id:{0}".format(id))  # Share
                        button3 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

                        if load_media.startswith("TrueNEXT"):
                            obj = load_media.split(":")[1]
                            button = telebot.types.InlineKeyboardButton(text=">>",
                                                                        callback_data=
                                                                        'load_fav {0} id:{1}'.format(obj,
                                                                                                     id))  # load more
                            button4 = telebot.types.InlineKeyboardButton(text="❌",
                                                                         callback_data=
                                                                         "favorite_del={id}&fav_command=TrueNEXT:{obj}".format(
                                                                             id=id, obj=obj))
                            keyboard.row(button2, button3)
                            keyboard.add(button4)
                            keyboard.add(button)

                        else:
                            keyboard.row(button2, button3)
                            keyboard.add(redo_btn)
                        bot.edit_message_caption(caption="File ID: {0} add back to your favorites".format(id),
                                                 message_id=call.message.message_id, chat_id=cid,
                                                 reply_markup=keyboard)

                    else:
                        if load_media == "":
                            keyboard.row(button, button3, button5, button41)

                        else:
                            keyboard.row(button, button3, button5, button42)
                            keyboard.add(button2)

                        bot.edit_message_reply_markup(cid, call.message.message_id, reply_markup=keyboard)

                except Exception as e:
                    msg = "Woops, I couldn't update your buttons, but don't worry! Your favorite was saved."
                    bot.answer_callback_query(call.id, text=msg, show_alert=True)
                    print("An Error occurred when tried to update the fav_btn:", e)
                    pass

            except ValueError:
                msg = "You already reached your limit of favorites! Go to /favorites to remove some, or" \
                      "contact @MrHalk for a premium account!"

                bot.answer_callback_query(call.id, text=msg, show_alert=True)

            except Exception as e:
                msg = "Woops, something went wrong! Please try to add this favorite again."
                bot.answer_callback_query(call.id, text=msg, show_alert=True)
                print("An Error occurred when tried to add a favorite for the user {0}:".format(cid), e)
                pass

        elif func == 'favorite_del':
            try:
                if id not in match:
                    bot.answer_callback_query(call.id, text="This file was already removed from favorites.")
                else:
                    Data.del_favorites(str(cid), id)
                    bot.answer_callback_query(call.id, text="Removed from favorites")

                try:
                    load = Img.search_query("id:{0}".format(id))  # Loads the json object with the query

                    dirc = load[0]['directory']

                    img = load[0]['image']

                    download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                    button = telebot.types.InlineKeyboardButton(text="💾", url=download_url)  # Download button
                    button2 = telebot.types.InlineKeyboardButton(text="➕",
                                                                 callback_data=
                                                                 load_media + "id={0}".format(id) + 'fav=No')  # load more
                    button3 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                 switch_inline_query='id:{0}'.format(id))  # Share
                    button41 = telebot.types.InlineKeyboardButton(text="⭐️",
                                                                  callback_data='favorite_add={id}'.format(id=id))
                    button42 = telebot.types.InlineKeyboardButton(text="⭐️",
                                                                  callback_data='favorite_add={id}&media={md}'.format(
                                                                      id=id,
                                                                      md=load_media))
                    button5 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))

                    if load_media.startswith("True"):

                        undo_btn = telebot.types.InlineKeyboardButton(text="Undo",
                                                                      callback_data=
                                                                      "favorite_add={id}&fav_command=True".format(
                                                                          id=id))
                        if load_media.startswith("TrueNEXT"):
                            obj = load_media.split(":")[1]
                            next_button = telebot.types.InlineKeyboardButton(text=">>",
                                                                             callback_data=
                                                                             'load_fav {0} id:{1} is_deleted'.format(obj,id))  # load more
                            keyboard.add(undo_btn)
                            keyboard.add(next_button)

                        else:
                            keyboard.add(undo_btn)
                        bot.edit_message_caption(caption="File ID: {0} removed from your favorites".format(id),
                                                 message_id=call.message.message_id, chat_id=cid,
                                                 reply_markup=keyboard)

                    else:
                        if load_media == "":
                            keyboard.row(button, button3, button5, button41)

                        else:
                            keyboard.row(button, button3, button5, button42)
                            keyboard.add(button2)

                        bot.edit_message_reply_markup(cid, call.message.message_id, reply_markup=keyboard)

                except Exception as e:
                    msg = "Woops, I couldn't update your buttons, but don't worry! Your favorite was saved."
                    bot.answer_callback_query(call.id, text=msg, show_alert=True)
                    print("An Error occurred when tried to update the fav_btn:", e)
                    pass

            except Exception as e:
                msg = "Woops, something went wrong! Please try to remove this favorite again."
                bot.answer_callback_query(call.id, text=msg, show_alert=True)
                print("An Error occurred when tried to remove a favorite for the user {0}:".format(cid), e)
                pass


@bot.message_handler(commands=['favs', 'fav', 'favorites'])
def send_favorites(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    try:
        user = Data.search_favorites(str(cid))
        user_favorites = user['favorites']
        limit = user['limit']
        count_favs = len(user_favorites)

        if limit == "None":
            limit_message = u'You are _Premium Member_, no limits applicable to your favorites'

        else:
            limit_message = u'You still can add _{limit}_ files to your favorites'.format(limit=limit)

        msg = u'*Favorites*\n\n' \
              u'You have _{count_favs}_  favorites.\n' \
              u'{limit_message}\n\n' \
              u'Tap the button below to view and manage your favorites.'.format(count_favs=count_favs,
                                                                                limit_message=limit_message)

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("View your favorites ({0})".format(count_favs),
                                                     callback_data="load_fav 0 is_init")
        keyboard.add(button1)

        bot.reply_to(m, msg, reply_markup=keyboard, parse_mode='markdown')

    except Exception as e:
        bot.reply_to(m, "Woops! Something weird happened. Please try again or contact @MrHalk for a bug report.")
        print("An exception occurred when tried to send 'user_fav_msg':", e)


@bot.callback_query_handler(func=lambda call: call.data.startswith("load_fav"))
def load_favs(call):
    if call.message:
        if call.data:
            splt = call.data.split()
            load_obj = int(splt[1])
            is_init = splt[2] if "is_init" in splt else ""
            is_deleted = splt[3] if "is_deleted" in splt else None
            previous_id = splt[2].split(":")[1] if splt[2].startswith("id:") else ""

            cid = call.message.chat.id

            try:
                user = Data.search_favorites(str(cid))
                user_favs = user['favorites']
                favs_count = len(user_favs)

                if load_obj >= favs_count:
                    bot.answer_callback_query(call.id, text="All favorites already loaded")

                else:
                    search_fav = user_favs[load_obj]

                    bot.send_chat_action(cid, 'upload_photo')  # Sends "uploading photo" chat action

                    load = Img.search_query("id:{0}".format(search_fav))  # Loads the json object with the query

                    # file = load['file_url']  # The picture url

                    id = load[0]['id']  # The picture unique identifier, on the server

                    dirc = load[0]['directory']

                    img = load[0]['image']

                    download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                    button = telebot.types.InlineKeyboardButton(text=">>",
                                                                callback_data=
                                                                'load_fav {0} id:{1}'.format(int(load_obj + 1),
                                                                                             search_fav))  # load more
                    button2 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                 switch_inline_query="id:{0}".format(id))  # Share
                    button3 = telebot.types.InlineKeyboardButton(text="ℹ️", callback_data="info={id}".format(id=id))
                    button4 = telebot.types.InlineKeyboardButton(text="❌",
                                                                 callback_data=
                                                                 "favorite_del={id}&fav_command=TrueNEXT:{obj}".format(id=id, obj=load_obj))

                    try:
                        if favs_count == int(load_obj + 1):
                            keyboard.row(button2, button3)
                            keyboard.add(button4)

                            bot.answer_callback_query(call.id, text="This is the last favorite. All favorites loaded.")

                        else:
                            keyboard.row(button2, button3)
                            keyboard.add(button4)
                            keyboard.add(button)

                        if img.endswith('.gif'):
                            bot.send_document(cid, download_url, caption='🎴ID: {id}\n'.format(id=id),
                                              reply_markup=keyboard)

                        else:
                            bot.send_photo(cid, download_url, caption='🎴ID: {id}\n'.format(id=id),
                                           reply_markup=keyboard)

                    except Exception as e:
                        bot.send_message(cid,
                                         'Sorry!\n`An unexpected error occurred when processing your request`.\n'
                                         'Please, try again',
                                         parse_mode='markdown', reply_to_message_id=call.message.message_id)
                        print("An Error occurred while loading a favorite:", e)

                    if is_init == "":
                        try:
                            if is_deleted is not None:
                                keyboard_ = telebot.types.InlineKeyboardMarkup()
                                undo_btn = telebot.types.InlineKeyboardButton(text="Undo",
                                                                              callback_data=
                                                                              "favorite_add={id}&fav_command=True".format(
                                                                                  id=id))
                                keyboard_.add(undo_btn)
                                bot.edit_message_reply_markup(cid, call.message.message_id, reply_markup=keyboard_)

                            elif previous_id is not "":
                                _keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                                _button2 = telebot.types.InlineKeyboardButton(text="🔘",
                                                                              switch_inline_query="id:{0}".format(
                                                                                  previous_id))  # Share
                                _button3 = telebot.types.InlineKeyboardButton(text="ℹ️",
                                                                              callback_data="info={id}".format(
                                                                                  id=previous_id))
                                _button4 = telebot.types.InlineKeyboardButton(text="❌",
                                                                              callback_data=
                                                                              "favorite_del={id}&fav_command=True".format(
                                                                                  id=previous_id)
                                                                              )

                                _keyboard.row(_button2, _button3)
                                _keyboard.add(_button4)

                                bot.edit_message_reply_markup(cid, call.message.message_id, reply_markup=_keyboard)

                            else:
                                pass

                        except Exception as e:
                            msg = "Woops, I couldn't update your buttons."
                            bot.answer_callback_query(call.id, text=msg, show_alert=True)
                            print("An Error occurred when tried to update the fav_menu_btn:", e)
                            pass

            except Exception as e:
                bot.send_message(cid,
                                 'Sorry!\n`An unexpected error occurred when processing your request`.\n'
                                 'Please, try again',
                                 parse_mode='markdown', reply_to_message_id=call.message.message_id)
                print("An Error occurred while loading a favorite:", e)
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

            # file = load[0]['file_url']  # File url
            id = load[0]['id']  # File unique identifier in the server
            dirc = load[0]['directory']  # Directory where it is stored in the server
            hash = load[0]['hash']  # The hash string provided by the server
            img = load[0]['image']
            thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)  # A complicated thumbnail
                                                                                               # builder
            tags = load[0]["tags"].split()  # Splits the tags in a list
            tags1 = tags[0]                 # These are just
            tags2 = tags[1]                 # to load up to
            tags3 = tags[2]                 # three tags

            rating = load[0]["rating"]                  # This one is tricky..
            if rating == "s":                           # It's meant to be
                tag_rating = "rating:safe"              # a reinforcement to
            elif rating == "q":                         # the Tags, so we have
                tag_rating = "rating:questionable"      # more control at similar
            else:                                       # Files for the user
                tag_rating = "rating:explicit"

            download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

            kb = types.InlineKeyboardMarkup()
            # kb1 = types.InlineKeyboardButton(text="💾", url=file)
            kb2 = types.InlineKeyboardButton(text="🔍 Search Similar",
                                             switch_inline_query_current_chat="{0} {1} {2} {3}".format(tag_rating,
                                                                                                       tags1,
                                                                                                       tags2,
                                                                                                       tags3))
            kb.add(kb2)

            pic_caption = 'Shared Picture\n🎴ID: {id}\n'.format(id=id)
            gif_caption = 'Shared GIF\n🎴ID: {id}\n'.format(id=id)
            if img.endswith('.gif'):  # if the file is a gif
                gif = types.InlineQueryResultGif('1', download_url, download_url, caption=gif_caption,
                                                 reply_markup=kb)
                result.append(gif)  # inserts the object in the cache database

            else:  # if the file is any type of image
                pic = types.InlineQueryResultPhoto('1', download_url, thumb, caption=pic_caption,
                                                   reply_markup=kb)
                result.append(pic)  # inserts the object in the cache database

            bot.answer_inline_query(inline_query.id, result, switch_pm_text="Your file is ready to be shared",
                                    switch_pm_parameter="share&id:{0}".format(id), is_personal=True)

            Data.update_inline_processed()

        else:  # if it is a normal query
            cache_list = []  # This is the cache database the bot will send
            af = 0

            for i in load:  # this 'for' loop inserts on the 'cache_list' up to 50 objects for the query result
                # file = i['file_url']  # file url
                id = i['id']  # File unique identifier in the server
                dirc = i['directory']  # Directory where it is stored in the server
                hash = i['hash']  # The hash string provided by the server
                thumb = "http://gelbooru.com/thumbnails/{0}/thumbnail_{1}.jpg".format(dirc, hash)  # again, the odd
                                                                                                   # thumbnail stuff

                dirc = i['directory']

                img = i['image']

                download_url = 'http://gelbooru.com/images/{dirc}/{img}'.format(dirc=dirc, img=img)

                kb = telebot.types.InlineKeyboardMarkup(row_width=2)
                kb1 = telebot.types.InlineKeyboardButton(text="💾 Original", url=download_url)  # Download button
                kb2 = types.InlineKeyboardButton(text="🔍 Search more",
                                                 switch_inline_query_current_chat=text)
                kb.row(kb1, kb2)
                if img.endswith('.gif'):  # if the file is gif
                    gif = types.InlineQueryResultGif(str(int(af)), download_url, thumb_url=download_url,
                                                     caption='🎴ID: {id}\n'.format(id=id),
                                                     reply_markup=kb)
                    cache_list.append(gif)  # inserts the object in the cache
                else:  # if the file is any type of image
                    pic = types.InlineQueryResultPhoto(str(int(af)), download_url, thumb_url=thumb,
                                                       caption='🎴ID: {id}\n'.format(id=id),
                                                       reply_markup=kb)
                    cache_list.append(pic)  # inserts the object in the cache
                af += 1

            b = 1 + off_set  # Complicated stuff, this is for the offset
            bot.answer_inline_query(inline_query.id, cache_list, next_offset=b, cache_time=120,
                                    switch_pm_text="Usage help", switch_pm_parameter="tags")

            Data.update_inline_processed()

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
# ==============================================  End of Media Handling  ==============================================


@bot.callback_query_handler(func=lambda call: True)  # The other inline button calls
def callback_inline(call):
    if call.message:  # Processes only buttons from messages
        if call.data == "commands":
            match = Data.user_search(str(call.message.chat.id))

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
            match = Data.user_search(str(call.message.chat.id))

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
            match = Data.user_search(str(call.message.chat.id))

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
            match = Data.user_search(str(call.message.chat.id))

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
            match = Data.user_search(str(call.message.chat.id))

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
            message = "Registered users: {0}".format(1)

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


row = ['⌨ Hide Keyboard', '⌨ Esconder Teclado', '⌨ Ocultar teclado', '⌨ Tastatur ausblenden',
       '⌨ Спрятать клавиатуру', '⌨ Nascondi tastiera']
@bot.message_handler(func=lambda message: message.text in row)
def hide_kb(m):
    kb = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(m, "Done!", reply_markup=kb)


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


# ================================================  Loop the polling  =================================================
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
