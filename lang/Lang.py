#-'- English Language Messages -'-
#use from lang import EN

Lang = {
'English': {
    'CommandText': {
        'start':
            u'Hello *{name}*!\n\n'
            u'I am _{bot_name}_, your personal *Eastern Media Assistant*!\n'
            u'Please, send `/help` if you need, or `/commands` to see all my functions!\n'
            u'I can work inline, so you can call me anytime you want, by typing `@EmaRobot` and writing your tags\n'
            u'Take a look at the examples of inline usage in `/inline_help` \n\n'
            u'BETA build no. 0.8.1',
        'start_reg':
            u'Hello again *{name}*! How are you? if you need any help, see /help \n(｡･ω･｡)',
        'help':
            u'A little bit lost? Don\'t worry!\n'
            u'Use the buttons bellow to see specific help:',
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
            u'  To use me inline, just tap in your input field `@{bot_id}`, and the query\n'
            u'  message should appear, so you can type what you want me to search.\n\n'
            u'2. *Searching by Tags* [|?|](telegram.me/{bot_id}?start=tags)\n'
            u'  You can use tags to make a specific search within my source\n\n'
            u'3. *Matching results*\n'
            u'  As you tap your tags to search, some results may appear, in order\n'
            u'  for you sir to see and select the desired picture!\n\n'
            u'Done! Now you are a pro in `inline search`, sir! (≧▽≦)',
        'tags':
            u'Usage:\n'
            u'`@{bot_id} [tags]`\n'
            u'Example: `@{bot_id} nase_yaeka bra` - This will return few images that matches these tags\n\n',
        'source_id':
            u'You can use any combination of numbers, from `0` to `2465530` - This will return you a single image '
            u'that matches this id.\n\n'
            u'_(Keep in mind: don\'t try astronomical numbers, I have a big source, but it\'s not infinite!)_',
        'help_use':
            u'Right, {name}. It\'s very simple to use me! I\'ll help you setting things up.\n'
            u'First, you probably saw my command row, that row of commands that shows up when you tap that\n'
            u'little |/|, in your typing bar. as you click on it, it will show all the available commands at\n'
            u'me! Also, you can click [here to see all my Commands!](https://telegram.me/{bot_id}?start=commands)\n'
            u'As you select one of my commands, it will send its designed feature, for example:\n'
            u'  -`/anime` _will send you a random Anime picture_\n'
            u'  -`/tag` _let\'s you searching for a tag!_ [|?|](telegram.me/{bot_id}?start=tags)\n\n'
            u'You can also make an inline search in me! [|?|](telegram.me/{bot_id}?start=inline_search)\n'
            u'Just do the following:\n'
            u'`@{bot_id} nase_yaeka bra` - This will return few images that matches the tags `nase_yaeka` and `bra`.\n\n',
        },
    'keyboard': {
        'buttons': {
                'lang': '🌐 Language',
                'notif': '🔔 Notifications',
                'prefs': '⚠️ Preferences',
                'hide_kb': '⌨ Hide Keyboard'
            },
        'inline_buttons':{
                'more':'➕ More',
                'info':'ℹ️ Info',
                'downld':'💾 Download',
                'help':{
                    'usg_help': '❓ Usage Help',
                    'cmnds': '🌐 Commands',
                    'in_help': '❔ Inline Help',
                    'tags':'#⃣ Tags',
                    'src_id':'📁 Source ID'
                    },
            },
        'messages': {
                'Lang_pref':u'Please, select your language preference below:\n\n'
                            u'_More languages are coming soon!_',
                'Chosen_lang': 'Ok! your language is set to `English`.',
                'set_opt':'Choose an option:'
            }
        }
    },
    'Português': {
        'CommandText': {
            'start':
                u'Hello *{name}*!\n\n'
                u'I am _{bot_name}_, your personal *Eastern Media Assistant*!\n'
                u'Please, send `/help` if you need, or `/commands` to see all my functions!\n'
                u'I can work inline, so you can call me anytime you want, by typing `@EmaRobot` and writing your tags\n'
                u'Take a look at the examples of inline usage in `/inline_help` \n\n'
                u'BETA build no. 0.8.1',
            'start_reg':
                u'Olá novamente *{name}*! Como está? Se precisar de ajuda, veja /help \n(｡･ω･｡)',
            'help':
                u'Está um pouco perdido? Não se preocupe!\n'
                u'Use os botões abaixo para ajuda específica:',
            'commands':
                u'Aqui estão todos os meus `comandos`, senhor!\n\n'
                u'/anime - Envia imagens de _anime_ aleatórias\n'
                u'/ecchi - Envia imagens _ecchi_ aleatórias\n'
                u'/loli - Envia imagens de _lolis_ aleatórias\n'
                u'/hentai - Envia imagens _hentai_ aleatórias\n'
                u'/yuri - Envia imagens de _yuri_ aleatórias\n'
                u'`/id` - Procurar imagens pelo meu [ID de fonte](telegram.me/{bot_id}?start=source_id)🚫\n'
                u'`/tag` - Procurar por [Tag](telegram.me/{bot_id}?start=tags)🚫\n\n'
                u'Você também pode me usar inline! Veja /inline\_help para mais informações, senhor!\n\n\n'
                u'_Comandos com 🚫 ainda não estão funcionando._',
            'inline_help':
                u'Aqui estão algumas icas para usar meu modo `inline`, senhor:\n\n'
                u'1. *Usagem inline*\n'
                u'  Para me usar inline, digite no campo de digitação `@{bot_id}`, e a mensagem\n'
                u'  de pesquisa deve aparecer, então você pode inserir o que quer pesquisar.\n\n'
                u'2. *Pesquisa por Tags* [|?|](telegram.me/{bot_id}?start=tags)\n'
                u'  Você pode usar tags para fazer pesquisas específicas na minha fonte.\n\n'
                u'3. *Resultados Correspondentes*\n'
                u'  Assim que digitar suas tags, alguns resultados irão aparecer,\n'
                u'   para o senhor ver e selecionar a imagem desejada!\n\n'
                u'Pronto! Agora o senhor é profissional em `pesquisa inline`! (≧▽≦)',
            'tags':
                u'Uso:\n'
                u'`@{bot_id} [tags]`\n'
                u'Exemplo: `@{bot_id} nase_yaeka bra` - Isso retornará imagens que correspondem à pesquisa\n\n',
            'source_id':
                u'Você pode usar qualquer combinação de números, de `0` a `3265023` - Isso trará uma única imagem '
                u'que corresponde a esse ID.\n\n'
                u'_(Lembre-se: não tente números astronômicos, eu tenho uma fonte grande, mas não infinita!)_',
            'help_use':
                u'Ok, {name}. É bem fácil de me usar! Eu irei te ajudar.\n'
                u'Primeiro, você provavelmente viu minha lista de comandos, aquela que aparece quando você clica\n'
                u'naquele pequeno |/|, na sua barra de digitação. Quando você clica, irá mostrar todos os meus comandos\n'
                u'disponíveis! Você também pode clicar [aqui para ver todos os meus comandos!](https://telegram.me/{bot_id}?start=commands)\n'
                u'Assim que digitar / selecionar um dos meus comandos, ele irá enviar sua função, por exemplo:\n'
                u'  -`/anime` _enviará uma imagem de anime aleatória_\n'
                u'  -`/tag` _permite que você procure por uma tag!_ [|?|](telegram.me/{bot_id}?start=tags)\n\n'
                u'Você também pode fazer busca inline em mim! [|?|](telegram.me/{bot_id}?start=inline_search)\n'
                u'É bem simples, faça algo assim:\n'
                u'`@{bot_id} nase_yaeka bra` - Isso retornará algumas imagens que correspondem às tags `nase_yaeka` e `bra`.\n\n',
            },
    'keyboard': {
        'buttons': {
                'lang': '🌐 Idioma',
                'notif': '🔔 Notificações',
                'prefs': '⚠️ Preferências',
                'hide_kb': '⌨ Esconder Teclado'
                },
        'inline_buttons':{
                'more':'➕ Mais',
                'info':'ℹ️ Info',
                'downld':'💾 Baixar',
                'help':{
                    'usg_help': '❓ Ajuda de Uso',
                    'cmnds': '🌐 Comandos',
                    'in_help': '❔ Ajuda modo Inline',
                    'tags':'#⃣ Tags',
                    'src_id':'📁 ID de Origem'
                    },
                },
        'messages': {
                'Lang_pref':u'Por favor, selecione sua preferência de idioma abaixo:\n\n'
                            u'_Mais idiomas em breve!_',
                'Chosen_lang': 'Ok! Seu idioma está configurado para `Português`.',
                'set_opt':'Escolha uma opção:'
                }
        },
    },
    'Español': {

    },

    'Deutsche': {

    },
    'русский': {

    },
    'Italiano': {

    },
}
# u'/yaoi - Sends you a random _yaoi_ Picture'
      #  u'`/cosplay` - Sends you a random _cosplay_  Picture 🚫\n'
      #  u'`/ecosplay` - Sends you a random _ero cosplay_  Picture 🚫\n'

"""
u'4. *Specific Search*\n'
    u'  Sir, you can make specific searchs to find what type of file you\n'
    u'  want! see some usage examples:\n'
    u'  - `@{bot_id} pic [tags]`: This will send you only pics about the tag\n'
    u'  - `@{bot_id} vid [tags]`: This will send you only videos about the tag\n'
    u'  - `@{bot_id} gif [tags]`: This will send you only GIFs about the tag\n\n'
"""

if __name__=="__main__":
    print("imported!")
