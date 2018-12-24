# -*- coding: UTF-8 -*-

import json
import random
import urllib3
import re
import os
from spider import proxyIpSpider
from spider import ipSpider
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
爬取m3u8链接
"""
class M3u8Spider:

    def __init__(self, url):
        self.url = url

    def createProxyIpPool(self):
        # p = proxyIpSpider.ProxyIpSpider()
        p = ipSpider.IpSpider()
        if p.spider():
            return True
        else:
            exit('创建代理ip池失败')

    def getProxyUrl(self):
        ipInfo = []
        if os.access('db/ip_info.json', os.F_OK):
            if os.access('db/ip_info.json', os.R_OK):
                fp = open('db/ip_info.json', encoding='utf-8')
                ipInfolist = json.load(fp)
                ipInfo = random.choice(ipInfolist)
                fp.close()
            else:
                exit('代理ip信息文件不可读')
        else:
            exit('代理ip信息文件不存在')

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
        html = html.decode('utf-8')
        # 匹配链接
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        httpLinkList = re.findall(pattern, html)
        for httpLink in httpLinkList:
            if httpLink.find('.m3u8') > 0:
                m3u8UrlList.append(httpLink)
            elif httpLink.find('.js') > 0 or httpLink.find('.php') > 0:
                subRes = http.request('get', httpLink, headers = headers)
                subHtml = subRes.data
                subHtml = subHtml.decode('utf-8')
                subHttpLinkList = re.findall(pattern, subHtml)
                for subHttpLink in subHttpLinkList:
                    if subHttpLink.find('.m3u8') > 0:
                        m3u8UrlList.append(subHttpLink)
        return m3u8UrlList


