import os
import json
import scrapy


FOLDER = os.getcwd() + '/storage/'
os.path.exists(FOLDER) or os.mkdir(FOLDER)

def write_json(file_path:str, file_value:dict) -> None:
    if os.path.exists(file_path):
        with open(file_path, "r") as file_json:
            data = json.load(file_json)
            data.append(file_value)
    else:
        data = [file_value]
    with open(file_path, 'w') as file_json:
        json.dump(
            data, 
            file_json, 
            indent=4,
        )

def get_cmp_id(file_path:str, key:str, search:int) -> bool:
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r") as file_json:
        data = json.load(file_json)
        presence = False
        for f in data:
            if f[key] == search:
                presence = True
    return presence


class ParseTwitterItem(scrapy.Item):
    # define the fields for your item here like:
    name = 'twitter_post'
    file_path = FOLDER + 'posts.json'
    name_twitter = scrapy.Field()
    name_link = scrapy.Field()
    post_link = scrapy.Field()
    post_date = scrapy.Field()
    post_stats = scrapy.Field()

    def process_item(self):
        dct = dict(self)
        if not dct['post_link']:
            return
        if not get_cmp_id(
            ParseTwitterItem.file_path, 
            'post_link', 
            dct["post_link"]
        ):
            write_json(
                ParseTwitterItem.file_path, 
                dct
            )