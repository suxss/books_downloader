# -*- coding: UTF-8 -*-
import requests
import re
import fake_useragent


class LanJuHua:
    headers = {'User-Agent': fake_useragent.UserAgent().random()}

    def __init__(self, proxy=None):
        self.proxies = proxy
        self.s = requests.Session()
        self.get_id()

    def get_id(self):
        url = 'http://www.lanjuhua.com/'
        req = self.s.get(url, headers=self.headers, proxies=self.proxies)
        self.id = re.findall(r'unique_uid=(.*?);', req.headers['Set-Cookie'])[0]

    def search(self, word, page=1):
        url_1 = 'http://www.lanjuhua.com/do.php'
        data = {'id': self.id, 'k': word}
        req_1 = self.s.post(url_1, data=data, headers=self.headers, proxies=self.proxies)
        url_2 = req_1.url
        key = re.findall(r's/([^/]*?)/', url_2)[0]
        url = f'http://www.lanjuhua.com/iajax.php?item=search&action=search_file_list&k={key}&id={self.id}&sEcho=1&iColumns=2&sColumns=%2C&iDisplayStart={(page-1)*25}&iDisplayLength=25&mDataProp_0=0&mDataProp_1=1'
        req = self.s.get(url, headers=self.headers, proxies=self.proxies)
        j = req.json()
        result = {'name': [], 'fid': []}
        for item in j['aaData']:
            x = re.findall(r'<a target="_blank" href="(.*?)">(.*?)</a>', item[0])
            ifid = x[0][0].split('/')[-1]
            iname = x[0][1]
            result['name'].append(iname)
            result['fid'].append(ifid)
        return result

    def get_dow_link(self, fid):
        url = f'http://www.lanjuhua.com/get_file_info.php?id={self.id}&fid={fid}/'
        req = self.s.get(url, headers=self.headers, proxies=self.proxies)
        j = req.json()
        return j['downurl']

