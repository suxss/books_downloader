import requests
import re
import fake_useragent
import json


def dict_to_json(dic):
    j = json.dumps(dic, indent=4, ensure_ascii=False)
    with open('top250.json', 'w', encoding='utf-8') as f:
        f.write(j)


class DouBan:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate'}

    def __init__(self, proxy=None):
        self.proxies = proxy

    def get_top_250(self):
        url = 'https://book.douban.com/top250?start='
        j = {'name': [], 'pic': []}
        for i in range(10):
            url_1 = url + str(25*i)
            req = requests.get(url_1, headers=self.headers, proxies=self.proxies)
            list_1 = re.findall(r'<img src="([^"]*?)" width="90" />\s*?</a>\s*?</td>\s*?<td valign="top">\s*?<div class="pl2">\s*?<a href=".*?" onclick=.*?; title="([^"]*?)"\s*?>', req.text)
            # print(list_1)
            j['pic'].extend([x[0] for x in list_1])
            j['name'].extend([x[1] for x in list_1])
        for i in range(len(j['name'])):
            j['name'][i] = re.sub('[(（].*?[)）]', '', j['name'][i])
        dict_to_json(j)
