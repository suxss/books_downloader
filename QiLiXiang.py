import requests
import fake_useragent


class QiLiXiang:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}

    def __init__(self, proxy=None):
        self.proxy = proxy

    def search(self, word, page=1):
        url = f'http://lxqnsys.com/pdf/php/getbooklist.php?channelid=search&pagenum={page}&sorttype=new&searchword={word}'
        r = requests.get(url, headers=self.headers, proxies=self.proxy)
        j = r.json()
        result = {'name': [item['bookname'] for item in j[1]['list']], 'author': [item['bookauthor'] for item in j[1]['list']], 'url': [item['bookurl'] for item in j[1]['list']]}
        return result
