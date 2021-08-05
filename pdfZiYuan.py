# -*- coding: UTF-8 -*-
import requests
import re
import fake_useragent
import CtCloud


class pdfZY:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word, page=1):
        url = f'http://pdf.018zy.com/page/{page}?s={word}'
        req_1 = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(r'<h2 class="m_post_top_title"><a href="(.*?)" title="(.*?)"', req_1.text)
        result = {'url': [x[0] for x in list_1], 'name': [x[1] for x in list_1]}
        return result

    def get_dow_link(self, url):
        req_1 = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(r'href="(.*?)"  target="_blank">点击下载</a>', req_1.text)
        req_2 = requests.get(list_1[0], headers=self.headers, proxies=self.proxies)
        password = re.findall(r'<p>网盘密码：诚通网盘密码：(.*?)(&nbsp;)*?</p>', req_2.text)[0][0]
        link = re.findall(r'<a href="(.*?)" target="_blank"><font color="red">', req_2.text)[0]
        link = re.sub('https://.*?\.com', 'https://474b.com', link)
        ctcloud = CtCloud.CtCloud()
        return ctcloud.get_dow_url(link, password)
