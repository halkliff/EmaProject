# -*- coding:ascii -*-

import requests
import random
"""
=========== Site List with all the accessible websites ===========
    url: The access URL
    hashed_string(when applicable): for authorization in some API methods.
"""
SITE_LIST = {
    'konachan': {
        'url': "http://konachan.com",
        'hashed_string': "So-I-Heard-You-Like-Mupkids-?--{0}--"},

    'yandere': {
        'url': "https://yande.re",
        'hashed_string': "choujin-steiner--{0}--"},
    'gelbooru': {
        'url': "http://gelbooru.com"
        }
    }
"""
 =========== The API access parameters ===========
    posts_list: API param to access the post list, where all the media is
    tags_list: NOT IN USE - Used to check whether a tag exists.
"""
API_NAME = {
    'konachan': {
        'posts_list':
            '/post.json',
        'tags_list':
            '/tag.json?'},
    'yandere': {
        'posts_list':
            '/post.json',
        'tags_list':
            '/tag.json?'},
    'gelbooru': {
        'posts_list':
            '/index.php?page=dapi&s=post&q=index&json=1',
        'tags_list':
            ''
        }
    }

"""
 =========== All the applicable parameters to the API ===========
    limit: to limit the request JSON object to only 1 object
    tag_limit: NOT IN USE - limit removal for the tags, so the API can freely search in all available tags
    page: NOT IN USE - page id for Moebooru sites
    safe: Tag combination for safe posts
    login: NOT IN USE - username authentication
    password_hash: NOT IN USE - password hash used to authenticate user in Moebooru sites. uses the SITE_LIST
                   hashed strings.
    anime - hentai: params with tag combinations for the specific search. pid means the page id. Only use in
                    Gelbooru.
    search: Opened for tag input, to search.
"""
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
    'anime': {
        'pid': list(range(329934)),
        'params': '&tags=rating%3Asafe&ms=1&limit=1'},
    'ecchi': {
        'pid': list(range(272744)),
        'params': '&tags=rating%3Aquestionable&ms=1&limit=1'},
    'loli': {
        'pid': list(range(117779)),
        'params': '&tags=loli&limit=1'},
    'yuri': {
        'pid': list(range(86580)),
        'params': '&tags=yuri&limit=1'},
    'yaoi': {
        'pid': list(range(40294)),
        'params': '&tags=yaoi&limit=1'},
    'hentai': {
        'pid': list(range(389413)),
        'params': '&tags=rating%3Aexplicit+-webm&limit=1'},
    'sweater_dress': {
        'pid': list(range(682)),
        'params': '&tags=virgin_killer_sweater&limit=1'
    },
    'animal_ears': {
        'pid': list(range(254091)),
        'params': '&tags=animal_ears&limit=1'
    },
    'search':
        '&limit=50&tags=-webm+'
    }


class Requests:
    def __init__(self, site_name="konachan / yandere / gelbooru", api_name="posts_list / tags_list", site_url=None):
        self.site_name = site_name.lower()
        self.api_name = api_name.lower()
        self.site_url = site_url

        if site_name or api_name is not "":
            if site_name in list(SITE_LIST):
                self.site_url = SITE_LIST[site_name]['url']
            else:
                raise Exception("Check again the site_name")
            if api_name in list(API_NAME[site_name]):
                self.api_name = API_NAME[site_name][api_name]
            else:
                raise Exception("Check again the api_name")

    def post_list(self, params="", pid=None):
        self.params = params
        self.pid = pid
        if params not in PARAMS:
            if params is None:
                pass
            else:
                raise Exception("Invalid param {0}. Use a valid param.".format(params))
        else:
            a = requests.get(self.site_url + self.api_name + PARAMS[params]['params'] + '&pid={0}'.format(self.pid))
            posts = a.json()
            return posts  # Returns a JSON object containing the matching results.

    def query_list(self, tags="tags".replace(':', '%3A'), pid=None):
        self.tags = tags.replace(' ', '+')
        self.pid = pid
        if tags is None:
            b = requests.get(self.site_url + self.api_name)
        else:
            b = requests.get(self.site_url + self.api_name + PARAMS['search'] + tags + '&pid=' + pid)
        query = b.json()
        return query  # Returns a JSON object containing the matching results.


def post(arg=""):
    a = Requests('gelbooru', 'posts_list')
    rpid = random.choice(PARAMS[arg]['pid'])
    pid = rpid
    b = a.post_list(arg, pid)
    return b[0] if b is not None else None  # Returns a JSON object containing the matching results.


def search_query(tags="", pid=None):
    a = Requests('gelbooru', 'posts_list')
    if pid is None:
        p = 0
    else:
        p = pid

    b = a.query_list(tags, pid=str(p))

    return b  # Returns a list with JSON object containing the matching results.
