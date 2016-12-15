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

    #When new messages arrive TeleBot will call this function.

    for m in messages:
        if m.content_type == 'text':
             #print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        #print(str(m))


bot = telebot.TeleBot(TOKEN)  # register bot token
bot.set_update_listener(listener)  # register listener

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'], ) #triggers the message for /start command
def send_welcome(m):
    from tinydb import TinyDB, Query

    db = TinyDB('User_Database\db.json')

    def new_user(from_user_id, from_user_language, from_user_nsfw_choice):
        db.insert({'id': from_user_id, 'language': from_user_language, 'nsfw': from_user_nsfw_choice})

    def user_search(from_user_id):
        user = Query()
        a = db.search(user.id == from_user_id)
        return a
    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #button = types.KeyboardButton('1. Test')
    #button2 = types.KeyboardButton('2. Test')
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
                print(user_search(str(m.chat.id)))
                bot.reply_to(m, "Hello *{name}*! I've saved you in my database.".format(name=m.from_user.first_name),
                             parse_mode = 'markdown')
            except Exception:
                raise Exception
        else:
            try:
                #markup.add(button)
                #markup.add(button2)
                bot.reply_to(m, en.commandText['start'].format(name = m.from_user.first_name, bot_name=Config.BOT_NAME),
                        parse_mode='markdown',) #reply_markup=markup
            except Exception:
                print(Exception)
                pass

@bot.message_handler(commands=['help'])
def send_help(m):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    button = telebot.types.InlineKeyboardButton("❓ Usage Help", callback_data='help_use')
    button2 = telebot.types.InlineKeyboardButton("🌐 Commands", callback_data='commands')
    #button3 = telebot.types.InlineKeyboardButton("❔ Inline Help", callback_data='inline_help')
    button4 = telebot.types.InlineKeyboardButton("#⃣ Tags", callback_data='tags')
    #button5 = telebot.types.InlineKeyboardButton("📁 Source ID", callback_data='source_id')

    try:
        keyboard.add(button)
        keyboard.row(button2, button4)
        #keyboard.row(button3, button5)
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
"""
@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    try:
        bot.reply_to(m, en.commandText['inline_help'].format(bot_id=Config.BOT_ID), parse_mode='markdown',
                     disable_web_page_preview=True)
    except Exception:
        print("An Error occurred when processing command /inline_help:", Exception)
        pass
"""
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
                       reply_markup=keyboard)  # reply_markup=keyboard
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
                       reply_markup=keyboard)  # reply_markup=keyboard
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
                       reply_markup=keyboard)  # reply_markup=keyboard
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
                       reply_markup=keyboard)  # reply_markup=keyboard
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
        #elif call.data == "commands":
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

@bot.inline_handler(func= lambda m:True) #useless?
def query_text(inline_query):
    print(inline_query.from_user.first_name + ":" + inline_query.query)

    print(inline_query.query)
    try:
        load = Img.query(inline_query.query)
        print(load)
        id = load[0]
        picture = load[8]
        big_picture = load[7]
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


    except Exception:
        raise Exception

"""
    import requests
    import random
    from API.Img import Requests, Posts
    from API import acc_setup as acc
    l = Requests(username=acc.username, password_hash=acc.password_hash,site_name='yandere', api_name='posts_list', param='search')
    site = '{site_url}{api_name}{login}{password}{param}{tags}{limit}'.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                                                                              password=l.password_hash, param=l.param,
                                                                              tags=inline_query.text, limit=Img.PARAMS['tag_limit'])
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






    try:
        pic = 'https://files.yande.re/image/0075af0a6017dab498a055e736b681f2/yande.re%20376607%20animal_ears%20caster_%28fate_extra%29%20fate_extra%20fate_grand_order%20fate_stay_night%20hohaku%20japanese_clothes%20tail%20thighhighs.jpg'
        #r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('LOL'))
        #r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Yo'))
        #r3 = types.InlineQueryResultArticle('3', 'Try Hard', types.InputTextMessageContent('_Tryharding_', parse_mode='markdown'))
        r4 = types.InlineQueryResultPhoto('1', photo_url=pic, thumb_url=pic)
        bot.answer_inline_query(inline_query.id, [r4])
    except Exception as e:
        print("An error Ocurred:", e)
"""

@bot.message_handler(func=lambda message: True) #Handling keyboard buttons
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
