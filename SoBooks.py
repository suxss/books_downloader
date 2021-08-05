# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import re
from urllib import parse


class SoBooks:
    code = 990602
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Referer': 'https://sobooks.cc',
               'Accpet-Encoding': 'gzip'}


    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word, page=1):
        url = 'https://sobooks.cc/search/' + parse.quote(word) + '/page/' + str(page)
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        dic = {'name': [],
               'author': [],
               'url': []}
        if url == req.url:
            list_1 = re.findall(
                r'<h3> <a href="(https://sobooks.cc/books/.*?)" title="(.*?)" target="_blank">.*?</a> </h3> <p> <a href=".*?">(.*?)</a> </p>',
                req.text)
            for (x, y, z) in list_1:
                dic['name'].append(y)
                dic['author'].append(z)
                dic['url'].append(x)
        else:
            list_1 = re.findall(
                r'<h1 class="article-title"><a href=".*?">(.*?)</a> <span></span></h1>',
                req.text)
            list_2 = re.findall(
                r'<li><strong>作者：</strong>(.*?)</li>', req.text)
            dic['name'].append(list_1[0])
            dic['author'].append(list_2[0])
            dic['url'].append(req.url)
        return dic

    def get_book_link(self, url):
        self.data = {'e_secret_key': self.code}  # 微信公众号 So Read 回复暗号
        r = requests.post(url=url, headers=self.headers, data=self.data, proxies=self.proxies)
        list1 = re.findall(
            r'</a><a href="https://sobooks\.cc/go\.html\?url=(.*?)" rel="nofollow">城通网盘（备用）</a>',
            r.text)
        list2 = re.findall(
            r'<div class="e-secret"><b style="font-size:16px; color:#F00;">提取密码：(.*?)</b>',
            r.text)
        if len(list1) != 0:
            dic = {'url': list1[0],
                   'password': list2[0],
                   'platform': 'ct'}
        else:
            list1 = re.findall(
                r'<a href="https://sobooks\.cc/go\.html\?url=(https://sobooks\.lanzoui\.com/.*?||https://sobooks.lanzous.com/.*?)".*?>.*?</a>.*?<',
                r.text)
            list2 = re.findall(
                r'<a href="https://sobooks\.cc/go\.html\?url=(https://sobooks\.lanzoui\.com/.*?||https://sobooks.lanzous.com/.*?)".*?>.*?</a>(.*?)<',
                r.text)
            if len(list1) != 0:
                list1[0] = list1[0].replace('https://sobooks.', 'https://www.')
                if 'lanzous' in list1[0]:
                    list1[0] = list1[0].replace('lanzous', 'lanzoui')
                pwd = list2[0][1].replace('密码:', '')
                dic = {'url': list1[0],
                       'password': pwd,
                       'platform': 'lz'}
            else:
                list1 = re.findall(
                    r'蓝奏云盘：<a href="https://sobooks\.cc/go\.html\?url=(.*?)" rel="nofollow">',
                    r.text)
                list2 = re.findall(
                    r'城通网盘：<a href="https://sobooks\.cc/go\.html\?url=(.*?)" rel="nofollow">',
                    r.text)
                if len(list1) != 0:
                    dic = {'url': list1[0],
                           'password': None,
                           'platform': 'lz'}
                elif len(list2) != 0:
                    dic = {'url': list2[0],
                           'password': None,
                           'platform': 'ct'}
        return dic
