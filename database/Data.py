"""import requests
import os
import time
from tinydb import TinyDB, Query

data_path = 'gelbooru/{0}/db.json'
path_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9',
             'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9',
             'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
print("Grabber started. Checking the database..")

def checker():
    for path in path_list:
        return os.path.exists(data_path.format(path))
    if False:
        raise FileNotFoundError("The path {0} doesn't exists. Please create it.".format(data_path))
print("Database file found. Starting the Process...")
time.sleep(5)
def grabber():
    i = 0
    a = 0
    max_path = 39
    print("Processing the database.")
    num_page_max=2000
    pid_max = 77371

    while i <= num_page_max:
        path = path_list[int(a)]
        db = TinyDB(data_path.format(path))
        r = requests.get('http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=42&json=1&pid=' + str(int(i)))
        req = r.json()

        print("Page {0} Processed. Saving on database...".format(i))
        try:
            db.insert_multiple(req)
            print("Page {0} saved. 42 new entries successfully inserted on database.".format(i))
        except:
            print("An error occurred when saving Page {0} on database. Breaking Program now.".format(i))
            break
        i = i+1
        if i >= num_page_max:
            print("Directory {0} at full capacity. Changing to a new directory...".format(path))
            time.sleep(0.8)
            num_page_max = int(2000 + num_page_max)
            a = a+1
        if a > max_path:
            print("More directories are needed. Saving the page number...")
            l = open("store.txt", 'w')
            l.write("{0}".format(i))
            print("Page number saved. Breaking loop.")
            break
        if i >= pid_max:
            print("All the pages processed. Breaking loop...")
            break

    print("All pages successfully saved on database. Program finished.")



checker()
grabber()"""

from tinydb import TinyDB, Query  # database module

db = TinyDB('user/db.json')  # this is the path of the user database

def new_user(from_user_username, from_user_id, from_user_language, from_user_nsfw_choice):  # Func to insert user on database
    db.insert({'id': from_user_id, 'username':from_user_username, 'language': from_user_language, 'nsfw': from_user_nsfw_choice})

def user_search(from_user_id):  # Func to search user on database. Returns the dict if the user exists, and None if doesn't match
    user = Query()              # with anything. If the dict is empty, use new_user() func to register the user in the database.
    a = db.search(user.id == from_user_id)
    if len(a) >= 1:
        return a
    else:
        return None

match = user_search('123956344')
print(match[0]['language'])