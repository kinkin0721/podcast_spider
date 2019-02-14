# -*- coding: utf-8 -*-


import tools
import json
from podgen import Media, Podcast
import os
from datetime import timedelta


class Music163:
    def __init__(self, album_id):
        self.headers = {'referer': 'https://music.163.com/', 'Content-Type': 'application/x-www-form-urlencoded'}
        self.podcast = None
        self.album_id = album_id
        self.album_info_url = 'http://music.163.com/api/dj/program/byradio'
        self.album_url = 'https://music.163.com/djradio?id={}'

    def get_podcast(self):
        datas = {'radioId': self.album_id, 'limit': '1000', 'offset': '0'}
        webpage = tools.get_url_with_datas(self.album_info_url, datas, self.headers)
        album_info = json.loads(webpage.decode('utf-8'))
        if album_info['code'] == 200:
            album_info_data = album_info['programs'][0]['radio']

            self.podcast = Podcast()
            self.podcast.name = album_info_data['name']
            self.podcast.website = self.album_url.format(self.album_id)
            self.podcast.description = album_info_data['desc']
            self.podcast.language = 'cn'
            self.podcast.image = album_info_data['picUrl']
            self.podcast.generator = 'kanemori.getpodcast'
            self.podcast.explicit = False
            self.podcast.withhold_from_itunes = True

            for program in album_info['programs']:
                self.get_episode(program)

            path = './podcast/music163'
            if not os.path.exists(path):
                os.makedirs(path)

            self.podcast.rss_file(os.path.join(path, '{}.xml'.format(self.album_id)), minimize=True)
            print("「{}」が上手に焼きました".format(self.album_id))

    def get_episode(self, program):
        episode = self.podcast.add_episode()
        episode.id = str('music163_djradio_' + str(program['id']))
        episode.title = program['name']
        # print(self.podcast.name + '=====' + episode.title)
        # if 'intro' in detail:
        #     episode.summary = detail['intro'].replace('\r', '\\r').replace('\n', '\\n')
        episode.publication_date = tools.publication_time(program['createTime'])
        play_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(program['mainTrackId'])
        episode.media = Media(play_url, duration=timedelta(milliseconds=program['duration']), type='audio/mpeg')
        episode.position = 1

        return play_url




