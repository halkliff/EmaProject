#-'- English Language Messages -'-
#use from lang import bot_lang-EN
import html

#
#HTML:
#<b>bold</b>
#<i>italic</i>
#<pre>fixedsys</pre>
#<code>code</code>
#<a href="link">hyperlink</a>

commandText = {
    'start':
        u'Hello *{name}*!\n\n'
        u'I am _Emα_, your personal *Eastern Media Assistant*!\n'
        u'Please, send `/help` if you need, or `/commands` to see all my functions!\n'
        u'I can work inline, so you can call me anytime you want, by typing `@EmaRobot` and writing your tags\n'
        u'Take a look at the examples of inline usage in `/inline_help` \n\n'
        u'BETA build no. 0.5.1' ,
    'help':''
}

msg = {
    'Hi': "Hi | Hi! | Hello | Hello!"
}

if __name__=="__main__":
    print("imported!")