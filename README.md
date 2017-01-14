# EmaProject
Just a bot project based on PyTelegramBotAPI by etnoir

All the help you can give is welcome! :D

This bot should fetch Danbooru-like website's pictures and send to user.
## A simple, yet powerful

Ema - *Eastern Media Assistant* was made thinking on the ease-to-use feature. Coding here is simple, as much as is fast and powerful.

### Setting up the rockets!

To start the setup, you must do the following:

1. **Install all the needed stuff**:</br>
```$ pip install PyTelegramBotAPI --upgrade```</br>
```$ pip install tinydb --upgrade```
2. Open [Config.py](https://github.com/halkliff/EmaProject/blob/Beta-2/Config.py)
  - Change the value of ```TOKEN``` to the token given for you by [@BotFather](https://telegram.me/botfather)
  - Change the value of ```BOT_ID``` to your own bot ID, without the "@". _NOTE: IF YOU PUT THE "@", THE BOT MIGHT NOT WORK PROPERLY_
  - Change the value of ```BOT_NAME``` to the name you want your bot to have - Yes, you can rename your bot easily with it
  - Change the value of ```MASTER_ID``` to your own chat id.
  
Now you're all set! run ```Bot.py``` and watch your Ema-based bot working!


# Changelog
**Beta-7:**
  Version 0.9.x! (Beta 7)
  0.9x is here!

  * Complete change in the API
  * New Server API (Gelbooru)
  * Working inline mode

and much more! See all the changes [here](https://github.com/halkliff/EmaProject/releases/tag/0.9.1-Beta-7)

**Beta-6:**
  * Bug Fixes

**Beta-5:**
  * Fixed some issues and mispellings
  * Added /admin command to know the status
  * Register users in a database
  * Users now have multiple language choices and changeability of it's language in database
  * Inline mode deactivated until the real database is ready
  * Delete DE.py
  * Delete ES.py
  * Delete PT.py
  * Delete RU.py
  * Delete EN.txt

**Beta-4:**
  * Workout in inline mode
  * API now have a function that will search for tags
  * Correction of some mispelling

**Beta-3:**
  * Major changes in the [/API/Img.py](https://github.com/halkliff/EmaProject/blob/Beta-2/API/IMG.py)
  * New strings added for the answers in [/lang/EN.py](https://github.com/halkliff/EmaProject/blob/Beta-2/lang/EN.py)
  * Major changes into [Bot.py](https://github.com/halkliff/EmaProject/blob/Beta-2/Bot.py) to work with the new API

# Future Plans

- [x] Finish up the inline mode (Finally!!!)
- [ ] Update with the final version 1.x.x
- [x] Translate to *Portuguese, Deutsch, Italian, Russian,* and *Spanish* (Yay!)
- [ ] Start the Chatting bot Project (Yes, Ema will be able to talk with you in the future!)
- [x] Reduce at minimum the code repetitions, to follow the [DRY - Don't repeat yourself](https://en.wikipedia.org/wiki/Don't_repeat_yourself) rule.
- [x] Embraced most of Pep-8


# Special thanks:
[@DanialNoori94](telegram.me/danialnoori94) - Many, Many thanks! without you, this project would never be possible ❤️<br />
Special thanks to [@skyr75](t.me/skyr75), [@Blury](t.me/blury), [@zvizdapil](t.me/zvizdapil), and [@R3D_C0D3](t.me/r3d_c0d3) for translating All Ema strings, really thanks!!!
