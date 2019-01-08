# -*- coding: utf-8 -*-

import json
import requests
import pytz
from datetime import datetime
from time import sleep


def load_config(filename):
    with open(filename, encoding='utf-8') as file:
        text = file.read()
        js = json.loads(text)
        return js


def save_config(json_dict, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        text = json.dumps(json_dict, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        file.write(text)


def get_url(url, headers, retries=10):
    try:
        res = requests.get(url, headers=headers)
    except Exception as what:
        print(what, url)
        if retries > 0:
            sleep(5)
            return get_url(url, headers, retries-1)
        else:
            print('GET Failed {}'.format(url))
            raise
    return res.content


def get_headers():
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    return headers


def publication_time(time):
        timestamp = datetime.fromtimestamp(time / 1000)
        return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                        tzinfo=pytz.utc)


def save_m4a(path, text):
    file = open(path, "wt")
    file.write(text)
    file.close()
