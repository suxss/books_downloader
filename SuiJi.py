# -*- coding: UTF-8 -*-
import requests
import CtCloud
import fake_useragent
import re


class SuiJi:
    headers = {'User-Agnet': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word):
        url = 'https://pan.shudan.vip/operate-search-' + word + '.html'
        req_1 = requests.get(url, headers=self.headers)
        f = req_1.text
        a = re.findall(r'<a href="read-(.*?)" aria-label=".*?">', f)
        b = re.findall(r'<a href=".*?" aria-label="(.*?)">', f)
        result = {'name': [x for x in b],
                  'url': ['https://pan.shudan.vip/read-'+x for x in a]}
        return result

    def get_dow_link(self, url):
        req_1 = requests.get(url, headers=self.headers)
        list_1 = re.findall(r'<br>访问密码：(.*?)\s*?</font>', req_1.text)
        list_2 = re.findall(r'<a href="([^"]*?)\n" target="_blank">.*?</a></h3>', req_1.text)
        ctcloud = CtCloud.CtCloud()
        link = ctcloud.get_dow_url(list_2[0], list_1[0])
        return link
