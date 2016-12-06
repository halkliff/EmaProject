#-'- English Language Messages -'-
#use from lang import EN

commandText = {
    'start':
        u'Hello *{name}*!\n\n'
        u'I am _{bot_name}_, your personal *Eastern Media Assistant*!\n'
        u'Please, send `/help` if you need, or `/commands` to see all my functions!\n'
        u'I can work inline, so you can call me anytime you want, by typing `@EmaRobot` and writing your tags\n'
        u'Take a look at the examples of inline usage in `/inline_help` \n\n'
        u'BETA build no. 0.6.1' ,
    'help':
        u'A little bit lost? Don\'t worry!\n'
        u'Use the `buttons` bellow to see specific help:',
    'commands':
        u'Here are all my `commands`, sir!\n\n'
        u'/anime - Sends you a random _anime_  Picture\n'
        u'/ecchi - Sends you a random _ecchi_  Picture\n'
        u'/loli - Sends you a random _loli_  Picture\n'
        u'/hentai - Sends you a random _hentai_  Picture\n'
        u'/yuri - Sends you a random _yuri_  Picture\n'

        u'`/id` - Search picture by my [Source\'s ID](telegram.me/{bot_id}?start=source_id)🚫\n'
        u'`/tag` - Search by [Tag](telegram.me/{bot_id}?start=tags)🚫\n\n'
        u'You can also search me using inline! see /inline\_help for further info, sir!\n\n\n'
        u'_Commands with 🚫 aren\'t working yet._',
    'inline_help':
        u'Here are some tips to use my `inline` feature, sir:\n\n'
        u'1. *Inline Usage*\n'
        u'  To use me inline, just tap in your input field `@EmaRobot`, and the query\n'
        u'  message should appear, so you can type what you want me to search.\n\n'
        u'2. *Searching by Tags* [|?|](telegram.me/{bot_id}?start=tags)\n'
        u'  You can use tags to make a specific search within my source\n\n'
        u'3. *Matching results*\n'
        u'  As you tap your tags to search, some results may appear, in order\n'
        u'  for you sir to see and select the desired picture!\n\n'
        u'4. *Specific Search*\n'
        u'  Sir, you can make specific searchs to find what type of file you\n'
        u'  want! see some usage examples:\n'
        u'  - `@{bot_id} pic [tags]`: This will send you only pics about the tag\n'
        u'  - `@{bot_id} vid [tags]`: This will send you only videos about the tag\n'
        u'  - `@{bot_id} gif [tags]`: This will send you only GIFs about the tag\n\n'
        u'Done! Now you are a pro in `inline search`, sir! (≧▽≦)',
    '/start tags':
        u'Usage:\n'
        u'`@EmaRobot [tags]`\n'
        u'Example: `@{bot_id} nase_yaeka bra` - This will return few images that matches these tags\n\n',
    '/start source_id':
        u'You can use any combination of numbers, from `0` to `2465530` - This will return you a single image '
        u'that matches this id.\n\n'
        u'_(Keep in mind: don\'t try astronomical numbers, I have a big source, but it\'s not infinite!)_'

}


if __name__=="__main__":
    print("imported!")
