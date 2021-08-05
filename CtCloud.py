# -*- coding: UTF-8 -*-
import re
import requests
import fake_useragent


class CtCloud:
    headers = {'User-Agent': fake_useragent.UserAgent().random(),
               'Accept-Encoding': 'gzip'}
    serial_number = 1

    def get_dow_url(self, url, passcode=''):
        uid, fid = self.get_ids(url)
        if url.split('/')[3] in {'dir', 'd'}:
            result = self.get_dir_content(url, passcode)
            url2 = result['url'][0]
            filechk, fid = self.get_filechk_id(url2, passcode)
        elif url.split('/')[3] in {'file', 'f'}:
            filechk, fid = self.get_filechk_id(url, passcode)
        link = self.get_dowload_links(uid, fid, filechk)
        return link

    def get_ids(self, url):
        print(url)
        url = url.rstrip('/')
        url = url.rstrip('\\')
        ids = url.split('/')[-1]
        id_list = ids.split('-')
        uid = id_list[0]
        fid = id_list[1]
        return uid, fid

    def get_filechk_id(self, url, passcode):
        ids = url.split('/')[-1]
        ids = ids.strip()
        try:
            url1 = '''https://webapi.ctfile.com/getfile.php?path=f&f=''' + ids + \
                '''&passcode=''' + str(passcode) + '''&token=false&ref='''
            headers = {
                'User-Agent': fake_useragent.UserAgent().random(),
                'Referer': url,
                'Origin': 'https://474b.com/',
                'Accept-Encoding': 'gzip'}
            r = requests.get(url1, headers=headers)
            a = r.json()
            return a['file_chk'], a['file_id']
        except:
            url1 = '''https://webapi.ctfile.com/getfile.php?path=file&f=''' + ids + \
                   '''&passcode=''' + str(passcode) + '''&token=false&ref='''
            headers = {
                'User-Agent': fake_useragent.UserAgent().random(),
                'Referer': url,
                'Origin': 'https://474b.com/',
                'Accept-Encoding': 'gzip'}
            r = requests.get(url1, headers=headers)
            a = r.json()
            return a['file_chk'], a['file_id']

    def get_dir_content(self, url, passcode):
        s = url.split('/')
        host = s[0] + '//' + s[2]
        ids = s[-1]
        try:
            url1 = '''https://webapi.ctfile.com/getdir.php?path=dir&d=''' + ids + \
                   '''&passcode=''' + str(passcode) + '''&token=false&ref='''
            headers = {
                'User-Agent': fake_useragent.UserAgent().random(),
                'Referer': url,
                'Origin': 'https://474b.com/',
                'Accept-Encoding': 'gzip'}
            r = requests.get(url1, headers=headers)
            a = r.json()
            r.close()
            url2 = 'https://webapi.ctfile.com/' + a['url']
            r2 = requests.get(url2, headers=headers)
            b = r2.json()
            dic = {'name': [],
                   'url': []}
            for item in b['aaData']:
                list_1 = re.findall(r'href="(.*?)">(.*?)</a>', item[1])
                dic['name'].append(list_1[self.serial_number-1][1])
                dic['url'].append(host + list_1[self.serial_number-1][0])
            return dic
        except:
            url1 = '''https://webapi.ctfile.com/getdir.php?path=d&d=''' + ids + \
                   '''&passcode=''' + str(passcode) + '''&token=false&ref='''
            headers = {
                'User-Agent': fake_useragent.UserAgent().random(),
                'Referer': url,
                'Origin': 'https://474b.com/',
                'Accept-Encoding': 'gzip'}
            r = requests.get(url1, headers=headers)
            a = r.json()
            r.close()
            url2 = 'https://webapi.ctfile.com/' + a['url']
            r2 = requests.get(url2, headers=headers)
            b = r2.json()
            dic = {'name': [],
                   'url': []}
            for item in b['aaData']:
                list_1 = re.findall(r'href="(.*?)">(.*?)</a>', item[1])
                dic['name'].append(list_1[self.serial_number - 1][1])
                dic['url'].append(host + list_1[self.serial_number - 1][0])
            return dic

    def get_dowload_links(self, uid, fid, filechk):
        url = "https://webapi.ctfile.com/get_file_url.php?uid=" + \
            str(uid) + "&fid=" + str(fid) + "&folder_id=0&file_chk=" + str(filechk) + "&mb=0&app=0&acheck=1"
        r = requests.get(url, headers=self.headers)
        a = r.json()
        # print(url)
        return a['downurl']
