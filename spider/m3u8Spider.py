# -*- coding: UTF-8 -*-

import json
import random
import urllib3
import re
from spider import proxyIpSpider

"""
爬取m3u8链接
"""
class M3u8Spider:

    def __init__(self, url):
        self.url = url

    def createProxyIpPool(self):
        p = proxyIpSpider.ProxyIpSpider()
        p.spider()

    def getProxyUrl(self):
        fp = open('db/ip_info.json', encoding = 'utf-8')
        ipInfolist = json.load(fp)
        ipInfo = random.choice(ipInfolist)
        return ipInfo['protocol'].lower() + '://' + ipInfo['ip'] + ':' + ipInfo['port']

    def getUserAgent(self):
        userAgentList = [
            'Mozilla/5.0 (Linux; Android 8.1; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070336) NetType/WIFI Language/zh_CN Process/tools',
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; MI 8 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.8.998 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        ]
        return random.choice(userAgentList)

    def getM3u8List(self, proxyUrl, headers):
        m3u8UrlList = []
        if proxyUrl == '':
            http = urllib3.PoolManager()
        else:
            http = urllib3.ProxyManager(proxyUrl)
        res = http.request('get', self.url, headers = headers)
        html = res.data
        return html
        # 匹配m3u8链接
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.m3u8')
        m3u8UrlList = re.findall(pattern, html)
        return m3u8UrlList


