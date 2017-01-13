# -*- coding: utf-8 -*-

import requests
import random


from API import acc_setup as acc

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
            '/tag.json?'

    }

PARAMS = {
    'limit':
        '&limit=1',
    'tag_limit':
        '&limit=0',
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
        '&tags=yaoi+',
    'for_hentai':
        '&tags=rating%3Aexplicit',
    'search':
        '&tags=order%3Arandom+'
    }
generic_url = '{site_url}{api_name}{login}{password}{param}{page}{limit}'

class Requests:
    def __init__(self, username="", password_hash="", site_name="", api_name="", param="", site_url=None):

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
            elif param == 'None':
                pass
            else:
                raise Exception("Check again the param")
        else:
            raise Exception("Woops, don't forget to fulfill site_name, api_name and the param.")

        if username and password_hash is not "":
            if username in acc.username:
                self.username = PARAMS['login'].format(username=username)
            else:
                raise Exception("Username not found")
            if password_hash in acc.password_hash:
                self.password_hash = PARAMS['password_hash'].format(password_hash=password_hash)
            else:
                raise Exception("Wrong Password Hash")
        else:
            self.password_hash = ""
            self.username = ""

class Posts:
    def __init__(self, id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width,
                 sample_height, preview_url):
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
        self.sample_width = sample_width
        self.sample_height = sample_height
        self.preview_url = preview_url


        #for the sake of consistency, if it doesn't exists, it uses the other
        if self.file_url is None:
            self.file_url = self.sample_url
        else:
            self.file_url = file_url

        if self.sample_url is None:
            raise Exception("Error: Image could not be found in the link", sample_url)
        if self.source is None:
            self.source = ""
        else:
            self.source = source


def anime():

    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
                 api_name='posts_list', param='for_anime')
    random_page = random.sample(range(1, 183363), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                                           password=l.password_hash, param=l.param, page='&page='+str(int(random_page_number)),
                                           limit=PARAMS['limit'])

    req = requests.get(url)


    ret = req.json()
    id = ret[0]["id"]
    tags = ret[0]["tags"]
    creator_id = ret[0]["creator_id"]
    author = ret[0]["author"]
    source = ret[0]["source"]
    score = ret[0]["score"]
    md5 = ret[0]["md5"]
    file_url = ret[0]["file_url"]
    sample_url = ret[0]["sample_url"]
    width = ret[0]["width"]
    height = ret[0]["height"]
    sample_width = ret[0]["sample_width"]
    sample_height = ret[0]["sample_height"]

    if width and height is None:
        width = sample_width
        height = sample_height
    else:
        pass

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width, sample_height, None)

    all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all

def ecchi():

    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
             api_name='posts_list', param='for_ecchi')
    random_page = random.sample(range(1, 108181), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                         password=l.password_hash, param=l.param, page='&page=' + str(int(random_page_number)),
                         limit=PARAMS['limit'])

    req = requests.get(url)

    ret = req.json()
    id = ret[0]["id"]
    tags = ret[0]["tags"]
    creator_id = ret[0]["creator_id"]
    author = ret[0]["author"]
    source = ret[0]["source"]
    score = ret[0]["score"]
    md5 = ret[0]["md5"]
    file_url = ret[0]["file_url"]
    sample_url = ret[0]["sample_url"]
    width = ret[0]["width"]
    height = ret[0]["height"]
    sample_width = ret[0]["sample_width"]
    sample_height = ret[0]["sample_height"]

    if width and height is None:
        width = sample_width
        height = sample_height
    else:
        pass

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width,
                sample_height, None)

    all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all

def loli():

    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
                 api_name='posts_list', param='for_loli')
    random_page = random.sample(range(1, 14921), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                             password=l.password_hash, param=l.param, page='&page=' + str(int(random_page_number)),
                             limit=PARAMS['limit'])

    req = requests.get(url)

    ret = req.json()
    id = ret[0]["id"]
    tags = ret[0]["tags"]
    creator_id = ret[0]["creator_id"]
    author = ret[0]["author"]
    source = ret[0]["source"]
    score = ret[0]["score"]
    md5 = ret[0]["md5"]
    file_url = ret[0]["file_url"]
    sample_url = ret[0]["sample_url"]
    width = ret[0]["width"]
    height = ret[0]["height"]
    sample_width = ret[0]["sample_width"]
    sample_height = ret[0]["sample_height"]

    if width and height is None:
        width = sample_width
        height = sample_height
    else:
        pass

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width,
                 sample_height, None)

    all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all

def hentai():

    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
                 api_name='posts_list', param='for_hentai')
    random_page = random.sample(range(1, 29486), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                             password=l.password_hash, param=l.param, page='&page=' + str(int(random_page_number)),
                             limit=PARAMS['limit'])

    req = requests.get(url)

    ret = req.json()
    id = ret[0]["id"]
    tags = ret[0]["tags"]
    creator_id = ret[0]["creator_id"]
    author = ret[0]["author"]
    source = ret[0]["source"]
    score = ret[0]["score"]
    md5 = ret[0]["md5"]
    file_url = ret[0]["file_url"]
    sample_url = ret[0]["sample_url"]
    width = ret[0]["width"]
    height = ret[0]["height"]
    sample_width = ret[0]["sample_width"]
    sample_height = ret[0]["sample_height"]

    if width and height is None:
        width = sample_width
        height = sample_height
    else:
        pass

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width,
                 sample_height, None)

    all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all

def yuri():

    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
                 api_name='posts_list', param='for_yuri')
    random_page = random.sample(range(1, 5027), 1)
    random_page_number = random_page[0]

    url = generic_url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                             password=l.password_hash, param=l.param, page='&page=' + str(int(random_page_number)),
                             limit=PARAMS['limit'])

    req = requests.get(url)

    ret = req.json()
    id = ret[0]["id"]
    tags = ret[0]["tags"]
    creator_id = ret[0]["creator_id"]
    author = ret[0]["author"]
    source = ret[0]["source"]
    score = ret[0]["score"]
    md5 = ret[0]["md5"]
    file_url = ret[0]["file_url"]
    sample_url = ret[0]["sample_url"]
    width = ret[0]["width"]
    height = ret[0]["height"]
    sample_width = ret[0]["sample_width"]
    sample_height = ret[0]["sample_height"]

    if width and height is None:
        width = sample_width
        height = sample_height
    else:
        pass

    data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width,
                 sample_height, None)

    all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height

    return all

def Query(tag):

    y = tag.split().replace(':', '%3A')
    l = Requests(username=acc.username, password_hash=acc.password_hash, site_name='yandere',
                 api_name='posts_list', param='search')

    _url = '{site_url}{api_name}{login}{password}{param}{tags}{limit}'

    url = _url.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                             password=l.password_hash, param=l.param, tags=y,
                             limit=PARAMS['tag_limit'])

    req = requests.get(url)

    ret = req.json()
    quantity = len(ret)
    if quantity == 0:
        return None
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
        preview_url = ret[num]["preview_url"]

        if width and height is None:
            width = sample_width
            height = sample_height
        else:
            pass

        data = Posts(id, tags, creator_id, author, source, score, md5, file_url, sample_url, width, height, sample_width, sample_height,
                     preview_url)

        all = data.id, data.tags, data.creator_id, data.author, data.source, data.score, data.md5, data.file_url, data.sample_url, data.width, data.height, data.preview_url

        return all

# Usage: 0: id, 1: tags, 2: creator_id, 3: author, 4: source, 5: score, 6: md5, 7: file_url,
# 8: sample_url, 9: width, 10:height, 11:preview_url
