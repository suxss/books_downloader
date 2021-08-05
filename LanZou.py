# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import re


def put_passcode(url, passcode):
    pwd = passcode
    header1 = {
        'User-Agent': fake_useragent.UserAgent().random(),
        'Referer': 'https://www.lanzoui.com/',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    header = {'User-Agent': fake_useragent.UserAgent().random(), 'Referer': url,
              'Accept-Encoding': 'gzip'}
    r1 = requests.get(url, headers=header1)
    result_1 = re.findall(
        r"type : 'post',\s*url : '/filemoreajax.php',\s*data : ([^。]*?),\s*dataType",
        r1.text)
    result_2 = re.findall(
        "var pgs;\n\tvar (.*?) = \'(.*?)\';\n\tvar (.*?) = (.*?);\n\tpgs =(.*?);\n",
        r1.text)
    r1.close()
    exec(result_2[0][0] + '=' + result_2[0][1])
    exec(result_2[0][2] + '=' + result_2[0][3])
    exec('pgs=' + result_2[0][4])
    result_1[0] = result_1[0].replace('\n', '')
    result_1[0] = result_1[0].replace('\t', '')
    a = eval(result_1[0])
    data = a
    data['uid'] = int(data['uid'])
    data['rep'] = int(data['rep'])
    r2 = requests.post(
        url='https://www.lanzoui.com/filemoreajax.php',
        data=data,
        headers=header)
    res = r2.json()
    r2.close()
    url1 = 'https://www.lanzoui.com/' + res['text'][0]['id']
    # res['info'] == "\u5bc6\u7801\u4e0d\u6b63\u786e"  密码不正确
    return url1


def get_file_info(url):
    data = {}
    header1 = {
        'User-Agent': fake_useragent.UserAgent().random(),
        'Accept-Encoding': 'gzip'}
    r1 = requests.get(url, headers=header1)
    list_1 = re.findall(
        r'<iframe class=".*?" name=".*?" src="(.*?)" frameborder="0" scrolling="no"',
        r1.text)
    url2 = 'https://www.lanzoui.com/' + list_1[-1]
    r1.close()
    s = requests.Session()
    r2 = s.get(url2, headers=header1)
    list_2 = re.findall(
        r'''<script type="text/javascript">\s*var (.*?) = ('[^。]*?');\s*var (.*?) = ('.*?');\s*''',
        r2.text)
    exec(list_2[0][0] + '=' + list_2[0][1])
    exec(list_2[0][2] + '=' + list_2[0][3])
    list_3 = re.findall(
        r'[^/]+?data\s*:\s*({.*?})\s*?,',
        r2.text)
    header2 = {
        'User-Agent': fake_useragent.UserAgent().random(),
        'Origin': 'https://www.lanzoui.com',
        'Referer': url2,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    r3 = s.post(url='https://www.lanzoui.com/ajaxm.php',
                headers=header2, data=eval(list_3[0]))
    j = r3.json()
    url3 = j['dom'] + '/file/' + j['url']
    r4 = s.head(url3, headers=header2)
    try:
        url3 = r4.headers['location']
    finally:
        return url3

