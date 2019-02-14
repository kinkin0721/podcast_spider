# -*- coding: utf-8 -*-

import time
from tools import load_config
import ximalaya
import music163


if __name__ == "__main__":
    albumlist = load_config('config.json')

    log = open("error.log", "a")
    for album in albumlist:
        try:
            if album['platform'] == 'ximalaya':
                podcast = ximalaya.Ximalaya(int(album['albumid']))
            if album['platform'] == 'music163':
                podcast = music163.Music163(int(album['albumid']))
            podcast.get_podcast()
        except Exception as e:
            print('异常:', e)
            curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log.write("{}：爬取{}的{}失败：{}\n".format(curr_time, album['platform'], album['albumid'], str(e)))

    print("肉が全部焼きました どうぞ")

