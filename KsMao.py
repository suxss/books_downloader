# -*- coding: UTF-8 -*-
import requests
import re
import fake_useragent
import LanZou


class KsMao:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def search(self, word):
        url = 'https://www.kuaisoumao.com/index/index/search?key=' + word
        req = requests.get(url, headers=self.headers, proxies=self.proxies)
        list_1 = re.findall(
            r'<div id="google-result-div" style="position: relative;">([\d\D]*?)<div id="result-panel-middle" class="result-panel-middle-show">',
            req.text)
        a = list_1[0].strip()
        a = a.replace(' ', '')
        list_2 = re.findall(
            r'<arel="noreferrerexternalnofollow"\nhref="('
            r'.*?)"\ntarget="_blank">\n<spanstyle="font-size:18px;font-family:arial,sans-serif;">\n('
            r'.*?)</span>\n</a>\n</div>\n<divclass="span-des">.*?</div>\n<divclass="span-host"style'
            r'="font-weight:bold;font-size:13px;">\n(.*?)</div>\n</div>\n</li>', a)

        dic = {'name': [],
               'url': [],
               'host': []}
        for (x, y, z) in list_2:
            if z not in {'https://cloud.189.cn', 'https://dev25.baidupan.com'}:
                dic['name'].append(y)
                dic['url'].append(x)
                dic['host'].append(z)
        return dic

    def get_down_link(self, url, host):
        if host in {'https://yueduyue1.com', 'https://ebookimg.lorefree.com/', 'https://kgbook.com/'}:
            return url
        elif 'lanzou' in host:
            return LanZou.get_file_info(url)


