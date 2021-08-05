# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import re


class KgBook:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word, page=1):
        url = 'http://www.kgbook.com/e/search/index.php'
        headers = self.headers
        headers['Referer'] = 'http://www.kgbook.com/'
        data = {'keyboard': word,
                'show': 'title,booksay,bookwriter',
                'tbname': 'download',
                'tempid': '1',
                'submit': '搜索'}
        s = requests.Session()
        req = s.post(url, headers=headers, data=data, proxies=self.proxies)
        url_1 = req.url + '&page=' + str(page-1)
        req.close()
        req_2 = requests.get(url_1, headers=headers, proxies=self.proxies)
        list_1 = re.findall(r'<h1><a href="(.*?)" >(.*?)</a></h1>', req_2.text)
        req_2.close()
        dic = {'name': [],
               'url': []}
        for (x, y) in list_1:
            dic['name'].append(y)
            dic['url'].append(x)
        return dic

    def get_down_link(self, url):
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(r'<a class="button" href="(.*?)">[^买]*?</a>', req.text)
        for i in range(len(list_1)):
            if 'GetDown?' in list_1[i]:
                list_1[i] = list_1[i].replace('GetDown?', 'GetDown/?')
            if '&amp;' in list_1[i]:
                list_1[i] = list_1[i].replace('&amp;', '&')
        req.close()
        headers = self.headers
        headers['Referer'] = url
        req_2 = requests.get(url=list_1[0], headers=headers, proxies=self.proxies)
        url = req_2.url
        req_2.close()
        return url
