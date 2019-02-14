# -*- coding: utf-8 -*-


import math
import json
from time import sleep
from podgen import Media, Podcast
import tools
import os
from datetime import timedelta


class Ximalaya:
    def __init__(self, album_id):
        self.headers = tools.get_headers()
        self.podcast = None
        self.album_id = album_id
        self.episode_pre_page = 30
        self.album_info_url = "https://www.ximalaya.com/revision/album?albumId={}"
        self.album_list_url = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&pageSize={}"
        self.episode_detail_url = "https://mobile.ximalaya.com/v1/track/baseInfo?trackId={}"
        self.album_url = "https://www.ximalaya.com/album/{}"

    def get_podcast(self):
        webpage = tools.get_url(self.album_info_url.format(self.album_id), self.headers)
        album_info = json.loads(webpage.decode('utf-8'))
        if album_info['ret'] == 200:
            album_info_data = album_info['data']

            self.podcast = Podcast()
            self.podcast.name = album_info_data['mainInfo']['albumTitle']
            self.podcast.website = self.album_url.format(self.album_id)
            if album_info_data['mainInfo']['richIntro']:
                self.podcast.description = album_info_data['mainInfo']['richIntro']
            self.podcast.language = 'cn'
            self.podcast.image = 'https:' + album_info_data['mainInfo']['cover'].split('!')[0]
            self.podcast.generator = 'kanemori.getpodcast'
            self.podcast.explicit = False
            self.podcast.withhold_from_itunes = True

            text = ''
            page_num = 1
            album_page_count = math.ceil(album_info_data['tracksInfo']['trackTotalCount'] / self.episode_pre_page) + 1
            while page_num <= album_page_count:
                webpage = tools.get_url(self.album_list_url.format(self.album_id, page_num, self.episode_pre_page),
                                        self.headers)
                album_list = json.loads(webpage.decode('utf-8'))
                for episode_info in album_list['data']['tracksAudioPlay']:
                    _, link = self.get_episode(episode_info['trackId'])
                    text += link

                page_num += 1

        path = './podcast/ximalaya'
        if not os.path.exists(path):
            os.makedirs(path)

        self.podcast.rss_file(os.path.join(path, '{}.xml'.format(self.album_id)), minimize=True)
        # tools.save_m4a(os.path.join(path, '{}.txt'.format(self.album_id)), text)
        print("「{}」が上手に焼きました".format(self.album_id))

    def get_episode(self, episode_id):
        trycount = 0
        findepisode = False

        while not findepisode:
            if trycount > 0:
                print("再接続中" + str(trycount) + "......")
            if trycount > 1:
                print("error url: " + self.episode_detail_url.format(episode_id) + "\n")
                return False, "error url: " + self.episode_detail_url.format(episode_id) + "\n"

            webpage = tools.get_url(self.episode_detail_url.format(episode_id), self.headers)
            detail = json.loads(webpage.decode('utf-8'))
            episode = self.podcast.add_episode()
            episode.id = str('ximalaya_' + str(episode_id))
            episode.title = detail['title']
            # print(self.podcast.name + '=====' + episode.title)
            if 'intro' in detail:
                episode.summary = detail['intro'].replace('\r', '\\r').replace('\n', '\\n')
            episode.publication_date = tools.publication_time(detail['createdAt'])
            episode.media = Media(detail['playUrl32'], duration=timedelta(milliseconds=detail['duration']))
            # episode.media = Media.create_from_server_response(detail['playUrl32'],
            #                                                   duration=timedelta(seconds=detail['duration']))
            episode.position = 1
            findepisode = True

            if not findepisode:
                trycount += 1
                print("30秒後に再接続する.......")
                sleep(30)

        return True, detail['playUrl32'] + '\n'


if __name__ == "__main__":
    test = Ximalaya(244444)
    test.get_podcast()


