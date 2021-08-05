# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import re
import json


def get_info(proxy=None):
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
    url = 'https://www.yuque.com/api/docs/share/608f68ae-debb-4b04-92c1-a702ffbf598f?doc_slug=ublg24&from=https://www' \
          '.yuque.com/docs/share/608f68ae-debb-4b04-92c1-a702ffbf598f?#%20%E3%80%8A%E6%97%A0%E6%A0%87%E9%A2%98%E3%80' \
          '%8B '
    req = requests.get(url, headers=headers, proxies=proxy)
    j = req.json()
    req.close()
    html = re.findall(r'>(\{.*})</span></p>', j['data']['content'])[0]
    escape_dict = {"&quot;": "\"", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&apos;": "'", "<p>": "  ",
                   "</p>": "\n"}
    for x, y in escape_dict.items():
        html = html.replace(x, y)
    d = json.loads(html)
    return d
