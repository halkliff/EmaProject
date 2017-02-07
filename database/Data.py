from tinydb import TinyDB, Query  # database module
from tinydb_smartcache import SmartCacheTable


# ================================================ Start of User Funcs ================================================

user_db = TinyDB('database/user/db.json')
user_db.table_class = SmartCacheTable
user_table = user_db.table('_default')


favs_db = TinyDB('database/user/user_favs/db.json')
favs_db.table_class = SmartCacheTable
favs_table = favs_db.table('_default')


def new_user(from_user_username, from_user_id, from_user_language):
    # Function to insert user on database. It must fill all the four arguments, or things could go bad on the bot
    user_table.insert({'id': from_user_id,
                       'username': from_user_username,
                       'language': from_user_language,
                       'nsfw': "No",
                       'notif': "Yes",
                       'user_is_premium': "No",
                       'user_blocked': "No"})
    favs_table.insert({'id': from_user_id,
                       'limit': 500,
                       'favorites': []})
                       


def user_search(from_user_id):
    # Func to search user on database. Returns the dict if the user exists, and None if doesn't match
    # with anything. If the dict is empty, use new_user() func to register the user in the database.
    user = Query()
    a = user_table.get(user.id == from_user_id)
    if a is not None:
        return a
    else:
        return None


def broadcast_append(cache_list):
    a = user_table.all()
    for i in a:
        cache_list.append(i['id'])


def mature_enabled_users(cache_list):
    a = []
    broadcast_append(a)

    for id in a:
        b = user_search(id)["nsfw"]
        if b == "Yes":
            cache_list.append(id)


def update_user_language(from_user_id, choice="Language"):
    user = Query()

    user_table.update({'language': choice}, user.id == from_user_id)


def toggle_stat_user_is_premium(from_user_id):
    user = Query()

    a = user_search(from_user_id)['user_is_premium']

    if a == "No":
        user_table.update({'user_is_premium': "Yes"}, user.id == from_user_id)
        favs_table.update({'limit': "None"}, user.id == from_user_id)

    else:
        user_table.update({'user_is_premium': "No"}, user.id == from_user_id)
        favs_quantity = favs_table.get(user.id == from_user_id)['favorites']
        count_favs = len(favs_quantity)

        if count_favs <= 500:
            limit = 500 - count_favs
        else:
            limit = 0

        favs_table.update({'limit': limit}, user.id == from_user_id)


def toggle_stat_user_blocked(from_user_id):
    user = Query()

    a = user_search(from_user_id)['user_blocked']

    if a == "No":
        user_table.update({'user_blocked': "Yes"}, user.id == from_user_id)

    else:
        user_table.update({'user_blocked': "No"}, user.id == from_user_id)


def toggle_stat_notifications(from_user_id):
    user = Query()

    a = user_search(from_user_id)['notif']

    if a == "No":
        user_table.update({'notif': "Yes"}, user.id == from_user_id)

    else:
        user_table.update({'notif': "No"}, user.id == from_user_id)


def toggle_stat_nsfw(from_user_id):
    user = Query()

    a = user_search(from_user_id)['nsfw']

    if a == "No":
        user_table.update({'nsfw': "Yes"}, user.id == from_user_id)

    else:
        user_table.update({'nsfw': "No"}, user.id == from_user_id)


def add_favorites(from_user_id, new_favorite):
    # Func to add a favorite on user database.

    user = Query()

    a = favs_table.get(user.id == from_user_id)
    limit = a['limit']
    favs = a['favorites']

    if limit == 0:
        raise ValueError("Limit reached")

    favs.append(new_favorite)
    if limit == "None":
        favs_table.update({'favorites': favs}, user.id == str(from_user_id))
    elif limit >= 0:
        favs_table.update({'favorites': favs, 'limit': int(limit - 1)}, user.id == str(from_user_id))


def del_favorites(from_user_id, rem_favorite):
    # Func to remove a favorite on user database

    user = Query()
    a = favs_table.get(user.id == from_user_id)
    limit = a['limit']
    favs = a['favorites']

    favs.remove(rem_favorite)
    if limit == "None":
        favs_table.update({'favorites': favs}, user.id == str(from_user_id))
    else:
        favs_table.update({'favorites': favs, 'limit': int(limit + 1)}, user.id == str(from_user_id))


def search_favorites(from_user_id):
    # Func to search the user's favorites. Returns a simple array of integers to be parsed to the web API

    user = Query()
    a = favs_table.get(user.id == from_user_id)

    if a is not None:
        return a
    else:
        return None

# ================================================ End of User Funcs ==================================================

# ============================================= Start of Statistics Funcs =============================================

stats_db = TinyDB('database/stats/db.json')
stats_db.table_class = SmartCacheTable
stats_table = stats_db.table('_default')


def get_stats():
    return stats_table.all()


def update_registered_users():
    user = Query()

    a = user_table.count(user.id is not None)

    stats_table.update({'registered_users': int(a)}, eids=[1])


def update_blocked_users():
    user = Query()

    a = user_table.count(user.user_blocked == "Yes")

    stats_table.update({'blocked_users': int(a)}, eids=[1])


def update_subscribed_users():
    user = Query()

    a = user_table.count(user.notif == "Yes")

    stats_table.update({'subscribed_users': int(a)}, eids=[1])


def update_muted_users():
    user = Query()

    a = user_table.count(user.notif == "No")

    stats_table.update({'muted_users': int(a)}, eids=[1])


def update_media_processed():

    a = get_stats()[0]['media_processed']

    b = a + 1

    stats_table.update({'media_processed': int(b)}, eids=[1])


def update_inline_processed():
    a = get_stats()[0]['inline_processed']

    b = a + 1

    stats_table.update({'inline_processed': int(b)}, eids=[1])

# ============================================= End of Statistics Funcs ==============================================

