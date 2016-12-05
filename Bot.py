# _||_ Code Test number 10 in utf-8 _||_
# Exclusive use

import telebot
from telebot import types
import logging
import time
import sys
from API import Img
from lang import EN as en

# Bot Token taken by @BotFather
TOKEN = '327068957:AAGvW-4w53Qo-ilN4dnoXy2-mlQ1UFOUhPg'


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
        bot.send_message(cid, en.commandText['/start tags'], parse_mode='markdown')
    elif text == "/start source_id":
        bot.send_message(cid, en.commandText['/start source_id'], parse_mode='markdown')
    else:
        try:
            bot.reply_to(m, en.commandText['start'].format(name = m.from_user.first_name),
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
        bot.reply_to(m, en.commandText['commands'], parse_mode='markdown')
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['inline_help'])
def send_inline_help(m):
    try:
        bot.reply_to(m, en.commandText['inline_help'], parse_mode='markdown')
    except Exception:
        print(Exception)
        pass

@bot.message_handler(commands=['anime'])
def send_anime(m):
    cid = m.chat.id
    load = Img.anime()
    picture = load[14]
    width = load[8]
    height = load[9]
    tag = load[11]
    uploader = load[3]
    if load[15] is None:
        large_file_url = load[14]
    else:
        large_file_url = load[15]


    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="Original {H} x {W}".format(H=height, W=width),
                                                url=large_file_url)
    button2 = telebot.types.InlineKeyboardButton(text="More", callback_data='generate')
    try:
        keyboard.add(button)
        keyboard.add(button2)

        bot.send_chat_action(cid, 'upload_photo')
        bot.send_photo(cid, picture,caption='Uploader:{uploader}\nTags: {tag}'.format(uploader=uploader,tag=tag[0, 1, 2],),
                       reply_markup=keyboard)
    except Exception:
        bot.send_message(cid, "Wasn't able to proceed your request.")
        print("An error Ocurred:", Exception)
        pass

@bot.message_handler(commands=['ecchi'])

@bot.message_handler(commands=['loli'])

@bot.message_handler(commands=['hentai'])

@bot.message_handler(commands=['yaoi'])

@bot.message_handler(commands=['yuri'])

@bot.message_handler(commands=['cosplay', 'ecosplay','id','tag'])
def send_nonworking_message(m):
    bot.reply_to(m, 'This command is not available yet :(')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
         if call.data == "generate":
            load = Img.anime()
            generate = load[14]
            width = load[8]
            height = load[9]
            tag = load[11]
            uploader = load[3]
            if load[15] is None:
                large_file_url = load[14]
            else:
                large_file_url = load[15]
            keyboard = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text="Original {H} x {W}".format(H=height, W=width),url=large_file_url)
            button2 = telebot.types.InlineKeyboardButton(text="More",
                                                         callback_data='generate')
            try:
                keyboard.add(button)
                keyboard.add(button2)
                bot.send_chat_action(call.message.id, 'upload_photo')
                bot.send_photo(call.message.chat.id, generate,
                                caption='Uploader:{uploader}\nTags: {tag}'.format(uploader=uploader,tag=tag[0, 1, 2],),
                                reply_markup=keyboard)
            except Exception:
                print("An error Ocurred:", Exception)
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
    bot.polling(none_stop=True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request.\n')
        sys.exit(0)

