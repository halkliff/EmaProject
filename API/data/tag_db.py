# -*- utf-8 -*-
# Tag database code

import random
from tinydb import Query, TinyDB
import requests
from API import Img

def grabber():
    l = Img.Requests(site_name='yandere', api_name='tags_list', param='limit')

    random_page = random.sample(range(1, 64075), 1)
    random_page_number = random_page[0]
    url = '{site_url}{api_name}{param}{page}'.format(site_url=l.site_url, api_name=l.api_name, login=l.username,
                                                                password=l.password_hash, param=l.param,
                                                     page='&page='+str(int(random_page_number)))

    req = requests.get(url)

    ret = req.json()
    db = TinyDB('db.json')
    db.insert(ret[0])

while True:
    try:
        grabber()
    except:
        print("Error")