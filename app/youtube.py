from __future__ import unicode_literals
import youtube_dl
import pdb


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def getmp3(link='https://youtu.be/TBNKyuYucR0?t=243', quality='192'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'download_archive': './dl_files/.archive',
        'outtmpl': './dl_files/%(id)s_%(title)s_.%(ext)s'
    }
    result = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        info_dict = ydl.extract_info(link, download=False)
        result['video_id'] = info_dict.get("id", None)
        result['video_title'] = info_dict.get('title', None)
    return result