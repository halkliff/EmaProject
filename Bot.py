# -*- utf-8 -*-
# _||_ Code Test number 14 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
from API import Img
from lang import EN as en
import Config

# Bot Token taken by @BotFather
TOKEN = Config.TOKEN


# Listener to see when new messages arrives
"""
def listener(messages):

    #When new messages arrive TeleBot will call this function.

    for m in messages:
        if m.content_type == 'text':
             #print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        #print(str(m))
""" #Activate this for debugging only

bot = telebot.TeleBot(TOKEN)  # register bot token
#bot.set_update_listener(listener)  # register listener. Use thhis only for debugging

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console. set 'logging.DEBUG' for debugging


@bot.message_handler(commands=['start'], ) #triggers the message for /start command
def send_welcome(m):
    from tinydb import TinyDB, Query

    db = TinyDB('database/user/db.json')

    def new_user(from_user_id, from_user_language, from_user_nsfw_choice):
        db.insert({'id': from_user_id, 'language': from_user_language, 'nsfw': from_user_nsfw_choice})

    def user_search(from_user_id):
        user = Query()
        a = db.search(user.id == from_user_id)
        return a
    text = m.text
    cid = m.chat.id
    match = user_search(str(m.chat.id))

    if text == "/start tags":
        try:
            bot.send_message(cid, en.commandText['/start tags'].format(bot_id=Config.BOT_ID),
                             parse_mode='markdown',)
        except Exception:
            print("An Error occurred when processing command /start tags:", Exception)
            pass

    if text == "/start source_id":
        try:
            bot.send_message(cid, en.commandText['/start source_id'], parse_mode='markdown',)
        except Exception:
            print("An Error occurred when processing command /start source_id:", Exception)

    if text == "/start commands":
        try:
            bot.reply_to(m, en.commandText['commands'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                         disable_web_page_preview=True)
        except Exception:
            print(Exception)
            pass

    else:
        if not match:
            try:
                new_user(str(m.chat.id), 'English', 'Yes')
                bot.reply_to(m, "Hello *{name}*! I've saved you in my database.".format(name=m.from_user.first_name),
                             parse_mode = 'markdown')
            except Exception:
                raise Exception
        else:
            try:
                bot.reply_to(m, en.commandText['start'].format(name = m.from_user.first_name, bot_name=Config.BOT_NAME),
                        parse_mode='markdown',)
            except Exception:
                print(Exception)
                pass

@bot.message_handler(commands=['help'])
def send_help(m):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    button = telebot.types.InlineKeyboardButton("❓ Usage Help", callback_data='help_use')
    button2 = telebot.types.InlineKeyboardButton("🌐 Commands", callback_data='commands')
    button3 = telebot.types.InlineKeyboardButton("❔ Inline Help", callback_data='inline_help')
    button4 = telebot.types.InlineKeyboardButton("#⃣ Tags", callback_data='tags')
    button5 = telebot.types.InlineKeyboardButton("📁 Source ID", callback_data='source_id')

    try:
        keyboard.add(button)
        keyboard.row(button2, button3)
        keyboard.row(button4, button5)
        bot.reply_to(m, en.commandText['help'], parse_mode='markdown', reply_markup=keyboard)
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['commands'])
def send_commands(m):
    try:
        bot.reply_to(m, en.commandText['commands'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                     disable_web_page_preview=True)
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    try:
        bot.reply_to(m, en.commandText['inline_help'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                     disable_web_page_preview=True)
    except Exception:
        print("An Error occurred when processing command /inline_help:", Exception)
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
                       reply_markup=keyboard)
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /anime:", Exception)
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
                       reply_markup=keyboard)
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /ecchi:", Exception)
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
                       reply_markup=keyboard)
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /loli:", Exception)
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
                       reply_markup=keyboard)
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred in /hentai:", Exception)
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

@bot.message_handler(commands=['cosplay', 'ecosplay','id','tag', 'inline_help'])
def send_nonworking_message(m):
    bot.reply_to(m, 'This command is not available yet :(')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message: # procees only buttons from messages
        if call.data == "anime":
            try:
                load = Img.anime()
            except Exception:
                retry_keyboard = telebot.types.InlineKeyboardMarkup()
                retry_button = telebot.types.InlineKeyboardButton(text="🔄 Retry", callback_data='retry_anime')
                retry_keyboard.add(retry_button)

                bot.reply_to(call.message.chat.id,
                             "Sorry!\n`An unexpected error occurred when processing your request`.\nTry again?", parse_mode='markdown',
                             reply_markup=retry_keyboard)

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
        elif call.data == "commands":
            try:
                bot.send_message(call.message.chat.id, en.commandText['commands'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception:
                print(Exception)
                pass
        elif call.data == "inline_help":
            try:
                bot.send_message(call.message.chat.id, en.commandText['inline_help'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception:
                print("An Error occurred when processing inline button [Inline Help]:", Exception)
                pass
        elif call.data == "tags":
            try:
                bot.send_message(call.message.chat.id, en.commandText['/start tags'].format(bot_id=Config.BOT_ID),
                                 parse_mode='markdown',)
            except Exception:
                print("An Error occurred when processing inline button [Tags]:", Exception)
                pass
        elif call.data == "source_id":
            try:
                bot.send_message(call.message.chat.id, en.commandText['/start source_id'], parse_mode='markdown',)
            except Exception:
                print("An Error occurred when processing inline button [Source ID]:", Exception)
                pass
        elif call.data == "help_use":
            try:
                bot.send_message(call.message.chat.id, en.commandText['help_use'].format(name=call.from_user.first_name,
                                                                                         bot_id=Config.BOT_ID, ),
                                 parse_mode='markdown', disable_web_page_preview=True)
            except Exception:
                print("An Error occurred when processing inline button[Usage Help]:", Exception)
"""
@bot.inline_handler(func= lambda m:True)
def query_text(inline_query):
    print(inline_query.from_user.first_name + ":" + inline_query.query)

    print(inline_query.query)
    try:
        load = Img.query(inline_query.query)
        print(load)
        id = load[0]
        picture = load[8]
        big_picture = load[7]                                       # ==> Inline not working yet.
        if big_picture is None:
            big_picture = load[8]
        width = load[9]
        height = load[10]
        tag = load[1]
        uploader = load[3]
        preview_url = load[11]
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton("💾 Download", url=big_picture)
            keyboard.add(button)
            r = types.InlineQueryResultPhoto(id, picture, preview_url, reply_markup=keyboard)

            bot.answer_inline_query(inline_query.id, r)
        except:
            pass
"""

    except Exception:
        raise Exception

def main_loop():
    #while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
        #else:
         #   break
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)
