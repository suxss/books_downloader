# -*- coding: UTF-8 -*-
import requests
import fake_useragent
import hashlib
import time
import random


def translate(word, fro='auto', to='auto'):
    """中文: zh-CHS, 英语: en,自动: auto"""
    a = fake_useragent.UserAgent().random()
    headers = {
        'User-Agent': a,
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cookie": "OUTFOX_SEARCH_USER_ID=1894454565@10.108.160.208; JSESSIONID=aaad-KV5kTKxWbvJYJ4Fx; " +
                  "OUTFOX_SEARCH_USER_ID_NCOO=984990548.44796; ___rl__test__cookies=1614782956571",
    }
    bv = '/'.join(a.split('/')[1:])
    bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
    ts = str(int(time.time() * 1000))
    salt = ts + str(random.randint(0, 9))
    sign = "fanyideskweb" + word + salt + "Tbh5E8=q6U3EXe+&L[4c@"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    data = {
        "smartresult": "dict",
        "version": "2.1",
        "doctype": "json",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTIME",
        "client": "fanyideskweb",
        'bv': bv,
        'salt': salt,
        'sign': sign,
        'lts': ts,
        'from': fro,
        'to': to,
        'i': word}
    r = requests.post(
        "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",
        data=data,
        headers=headers)
    j = r.json()
    r.close()
    return j['translateResult'][0][0]['tgt']
