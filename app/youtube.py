from __future__ import unicode_literals
import youtube_dl
import pdb
from app import app

MP3DIR = app.config['MP3DIR']


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    print(d)
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def getmp3(link, quality='192'):
    print("DEBUG: {}".format(MP3DIR))
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'download_archive': './app/{}/.archive'.format(MP3DIR),
        'outtmpl': './app/{}/%(id)s.%(ext)s'.format(MP3DIR)
    }
    print(ydl_opts)
    result = {}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info_dict = ydl.extract_info(link, download=False)
            result['video_id'] = info_dict.get("id", None)
            result['video_title'] = info_dict.get('title', None)
            result['error'] = ''
    except:
        result['error'] = "couldn't get video.  Check the URL is a video, then try again"
    return result

