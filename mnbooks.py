# -*- coding: UTF-8 -*-
import requests
import re
import fake_useragent
import CtCloud


class MNBooks:
    headers = {'User-Agnet': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word, page=1):
        url = 'https://www.manongbook.com/e/search/index.php'
        data = {'show': 'title,newstext',
                'tempid': '1',
                'keyboard': word}
        req_1 = requests.post(url, data=data, headers=self.headers)
        req_2 = requests.get(url=req_1.url+f'&page={page-1}', headers=self.headers)
        req_1.close()
        list_1 = re.findall(r'<i>\s*?<a href="(.*?)" title="(.*?)">\s*?<img src=".*?" alt=".*?" /></a>\s*?</i>', req_2.text)
        dict_1 = {'name': [x[1] for x in list_1], 'url': [x[0] for x in list_1]}
        return dict_1

    def get_dow_link(self, url):
        req_1 = requests.get(url, headers=self.headers)
        list_1 = re.findall(r'<a href="(.*?)" target="_blank"><span style="color:#FF0000;">点击下载</span></a></span>', req_1.text)
        req_1.close()
        req_2 = requests.get(url='https://www.manongbook.com/'+list_1[0], headers=self.headers)
        list_2 = re.findall(r'<a href="([^"]*?)" target="_blank"><span style="font-size:24px;">城通网盘下载（访问密码：(.*?)）</span></a>', req_2.text)
        ctcloud = CtCloud.CtCloud()
        link = ctcloud.get_dow_url(list_2[0][0], list_2[0][1])
        return link
