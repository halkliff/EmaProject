#Example API _-_UTF-8_-_

import requests
import random


SITE_LIST = {
    'konachan': {
        'url': "http://konachan.com",
        'hashed_string': "So-I-Heard-You-Like-Mupkids-?--{0}--"},

    'yandere': {
        'url': "https://yande.re",
        'hashed_string': "choujin-steiner--{0}--"}
    }

API_NAME={
        'posts_list':
            '/post.json?',
    'tags_list':
        '/tag.json'

    }

PARAMS = {
    'limit':
        '&limit=1',
    'page':
        '&page=',
    'safe':
        '&tags=rating%3Asafe',
    'login':
        'login={username}',
    'password_hash':
        '&password_hash={password_hash}',
    'for_anime':
        '&tags=rating%3Asafe+-pantyshot+-panties+&ms=1',
    'for_ecchi':
        '&tags=rating%3Aquestionable+&ms=1',
    'for_loli':
        '&tags=loli+',
    'for_yuri':
        '&tags=yuri+',
    'for_yaoi':
        '&tags=yaoi+'
    }

class Requests:
    def __init__(self, username="", password_hash="", site_name="", api_name="", param="", site_url=None):
        print("API initialized")

        self.site_name = site_name.lower()
        self.api_name = api_name.lower()
        self.param = param
        self.site_url = site_url
        self.username = username
        self.password_hash = password_hash

        if site_name is not "" or api_name is not "" or param is not "":
            if site_name in list(SITE_LIST):
                self.site_url = SITE_LIST[site_name]['url']
            else:
                raise Exception("Check again the site_name")
            if api_name in list(API_NAME):
                self.api_name = API_NAME[api_name]
            else:
                raise Exception("Check again the api_name")
            if param in list(PARAMS):
                self.param = PARAMS[param]
            else:
                raise Exception("Check again the api_name")
        else:
            raise Exception("Woops, don't forget to fulfill site_name, api_name and the param.")

        if username and password_hash is not "":
            if username in api_login_info.username:
                self.username = PARAMS['login'].format(username=username)
            else:
                raise Exception("Username not found")
            if password_hash in api_login_info.password_hash:
                self.password_hash = PARAMS['password_hash'].format(password_hash=password_hash)
            else:
                raise Exception("Wrong Password Hash")
        else:
            self.password_hash = '&password_hash=none'
            self.username = 'login=none'


class Posts:
    def __init__(self, id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, **kwargs):
        self.id = id
        self.tags = tags
        self.creator_id = creator_id
        self.author = author
        self.source = source
        self.score = score
        self.md5 = md5
        self.file_url = file_url
        self.sample_url = sample_url
        self.width = width
        self.height = height
        self.other_width = kwargs.get("jpeg_width")
        self.other_height = kwargs.get("jpeg_height")
        self.other_file_url = kwargs.get("jpeg_url")

        #for the sake of consistency, if it doesn't exists, it uses the other
        if width or height or file_url is None:
            self.width = self.other_width
            self.height = self.other_height
            self.file_url = self.other_file_url

        if sample_url is None:
            raise Exception("Error: Image could not be found in the link", sample_url)
        if source is None:
            self.source = "No Source could be found"

generic_url = '{site_url}{api_name}{login}{password}{param}{page}{limit}'

def anime():
    l = Requests(site_name='yandere',
                 api_name='posts_list', param='for_anime')
    random_page = random.sample(range(1, 183363), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                                           password=l.password_hash, param=l.param, page='&page='+str(int(random_page_number)),
                                           limit=PARAMS['limit'])
    print(url)
    req = requests.get(url)


    ret = req.json()
    id = ret["id"]
    tags = ret["tags"]
    creator_id = ret["creator_id"]
    author = ret["author"]
    source = ret["source"]
    score = ret["score"]
    md5 = ret["md5"]
    file_url = ret["file_url"]
    sample_url = ret["sample_url"]
    width = ret["width"]
    height = ret["width"]

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height)
    print(data)
    all = data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all
