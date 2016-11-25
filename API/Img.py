#Example API _-_UTF-8_-_

import requests
import random

class Requests:
    def __init__(self, id, created_at, uploader_id, uploader_name, score, source,
                 md5, rating, image_width, image_height, tag_string, tag_string_general,
                 tag_count_artist, pixiv_id, file_url, large_file_url, ):
        self.id = id
        self.created_at = created_at
        self.uploader_id = uploader_id
        self.uploader_name = uploader_name
        self.score = score
        self.source = source
        self.md5 = md5
        self.rating = rating
        self.image_width = image_width
        self.image_height = image_height
        self.tag_string = tag_string
        self.tag_string_general = tag_string_general
        self.tag_count_artist = tag_count_artist
        self.pixiv_id = pixiv_id
        self.file_url = file_url
        self.large_file_url = large_file_url



Danbooru = 'http://danbooru.donmai.us'
Dreq = requests.get(Danbooru + '/posts.json?&limit=2000000')

loaded_data = Dreq.json()

last_num = len(loaded_data)
random_list = random.sample(range(1, last_num), 1)
randomly_chosen_number = random_list[ 0 ]

r = requests.get(Danbooru + '/posts/' + str(loaded_data[ int(randomly_chosen_number) ][ "id" ]) + '.json')
data = Requests(r.json()["id"], r.json()["created_at"], r.json()["uploader_id"], r.json()["uploader_name"], r.json()["score"],
                    r.json()["source"], r.json()["md5"], r.json()["rating"], r.json()["image_width"], r.json()["image_height"],
                    r.json()["tag_string"], r.json()["tag_string_general"], r.json()["tag_count_artist"], r.json()["pixiv_id"],
                    r.json()["file_url"], r.json()["large_file_url"])

#==================================================================================================================
#Data Working for import
id = data.id
created_at = data.created_at
uploader_id = data.uploader_id
uploader_name = data.uploader_name
score = data.score
source = data.source
md5 = data.md5
rating = data.rating
image_width = data.image_width
image_height = data.image_height
tag_string = data.tag_string
tag_string_general = data.tag_string_general
tag_count_artist = data.tag_count_artist
pixiv_id = data.pixiv_id
file_url = data.file_url
large_file_url = data.large_file_url


if __name__=="__main__":
    print("Imported!")
