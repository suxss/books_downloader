# -*- coding: UTF-8 -*-
import threading
import requests
import fake_useragent
from urllib.parse import unquote, urlparse
import os


def split(start, end, step):
    parts = [(i, min(i + step, end)) for i in range(start, end, step)]
    return parts


def parse_filename(url):
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate',
               'Connection': 'Keep-Alive',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
    r = requests.head(url, headers=headers)
    d = r.headers
    if 'Location' in d and d['Location']:
        r = requests.head(d['Location'], headers=headers)
        r.encoding = 'utf-8'
        d = r.headers
    if 'Content-Disposition' in d and d['Content-Disposition']:
        disposition_split = d['Content-Disposition'].split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1].split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
                    filename = filename.strip('"')
                    filename = filename.strip("'")
                    return filename
    url = urlparse(url).path
    filename = url.split('/')[-1]
    try:
        filename = unquote(filename)
    except Exception as e:
        print(e)
    finally:
        filename = normalize(filename)
        filename = filename.strip('"')
        filename = filename.strip("'")
        return filename


def normalize(filename):
    for item in {'/', '\\', ':', '*', '?', '<', '>', '|'}:
        filename = filename.replace(item, '')
    return filename


class Download:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate',
               'Connection': 'Keep-Alive',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}

    def __init__(self, link, file_dir, file_name=None, name_mode=1, thread_num=1, proxy=None):
        self.s = requests.session()
        self.link = link
        if name_mode != 2 or not file_name:
            if not file_name:
                file_name = parse_filename(link)
            else:
                file_name = normalize(file_name)
        else:
            format = parse_filename(link).split('.')[-1]
            file_name = file_name + '.' + format
        if file_dir:
            file_dir = file_dir + '/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + file_name
        self.file_path = file_path
        self.thread_num = thread_num
        self.threads = []
        self.proxy = proxy

    def download(self):
        f = self.s.head(url=self.link, headers=self.headers, proxies=self.proxy)
        self.file_size = int(dict(f.headers).get('Content-Length', 0))
        f.close()
        current_part_size = self.file_size // self.thread_num + 1
        parts = split(0, self.file_size, current_part_size)

        if parts:
            for x, y in parts:
                t = open(self.file_path, 'wb')
                t.seek(x, 0)
                td = ThreadDownload(self.link, x, y, t, mode=1, proxy=self.proxy)
                self.threads.append(td)
                td.start()
        else:
            t = open(self.file_path, 'wb')
            t.seek(0, 0)
            td = ThreadDownload(self.link, 0, None, t, mode=0, proxy=self.proxy)
            self.threads.append(td)
            td.start()

    def get_complete_rate(self):
        sum_size = 0
        for i in range(len(self.threads)):
            sum_size += self.threads[i].length
        if self.file_size != 0:
            return sum_size / self.file_size
        else:
            return None


class ThreadDownload(threading.Thread):
    def __init__(self, link, start_pos, end_pos, current_part, mode, proxy=None):
        super().__init__()
        self.link = link
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_part = current_part
        self.length = 0
        self.mode = mode
        self.proxy = proxy

    def run(self):
        mode = self.mode
        headers = {'User-Agent': fake_useragent.UserAgent().random(),
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'Keep-Alive',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
                   }
        if mode:
            headers['Range'] = f'bytes={self.start_pos}-{self.end_pos}'
        f = requests.get(self.link, headers=headers, stream=True, proxies=self.proxy)
        chunk_size = 1024
        for chunk in f.iter_content(chunk_size=chunk_size):
            self.current_part.write(chunk)
            self.length += 1024
        self.current_part.close()
        f.close()
