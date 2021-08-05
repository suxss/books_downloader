# -*- coding: UTF-8 -*-
import re
import fake_useragent
import requests


class Bloogle:
    escape_dict = {'&raquo;': '>>', '&hellip;': '…', '&#038;': '&', '&nbsp;': ' ', "&quot;": "\"", "&amp;": "&",
                   "&lt;": "<", "&gt;": ">", "&apos;": "'"}

    def __init__(self, proxy=None):
        self.headers = {'User-Agent': fake_useragent.UserAgent().random(),
                        'Referer': 'https://bloogle.top/'}
        self.proxies = proxy

    def search(self, word, page=1):
        url = 'https://bloogle.top/page/' + str(page) + '/?s=' + word
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(
            r'搜索结果\s*?</h1>([\d\D]*?)<nav class="navigation pagination" role="navigation"',
            req.text)
        list_2 = re.findall(
            r'<h2 class="entry-title"><a href="(.*?)" rel="bookmark">(.*?)</a></h2>	</header>',
            list_1[0])
        dic = {'name': [],
               'url': []}
        for x in list_2:
            a = x[1]
            for item in self.escape_dict.keys():
                a = a.replace(item, self.escape_dict[item])
            dic['name'].append(a)
            dic['url'].append(x[0])
        return dic

    def get_down_url(self, url):
        req_1 = requests.get(url, self.headers, proxies=self.proxies)
        list_1 = re.findall(
            r'<div class="wp-block-button alignleft"><a class="wp-block-button__link" href="(.*?)">.*?下载</a></div>',
            req_1.text)
        return list_1[0]


if __name__ == '__main__':
    bloogle = Bloogle()
    a = bloogle.search('历史')
    print(a)
    b = bloogle.get_down_url(a['url'][0])
    print(b)
