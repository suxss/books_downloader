# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import re
import CtCloud


class Kindle8:
    headers = {'User-Agnet': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}
    code = 2788

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word, page=1):
        url = 'https://www.kindle8.cc/page/' + str(page) + '?s=' + word
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(r'<a rel="bookmark" href="(.*?)">(.*?)</a>', req.text)
        req.close()
        dic = {'name': [],
               'url': []}
        for i in range(len(list_1)):
            dic['name'].append(list_1[i][1])
            dic['url'].append(list_1[i][0])
        return dic

    def get_down_link(self, url):
        self.data = {'huoduan_verifycode': self.code}
        req = requests.post(url, data=self.data, headers=self.headers, proxies=self.proxies)
        html_1 = re.findall(r'<h3>.*?</h3>([\d\D]*?)</article>', req.text)[0]
        req.close()
        list_1 = re.findall(r'<a href="([^ ]*?)">', html_1)
        ctcloud = CtCloud.CtCloud()
        return ctcloud.get_dow_url(self.get_real_down_url(list_1[0]))

    def get_real_down_url(self, url):
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        return req.url
