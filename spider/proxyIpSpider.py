# -*- coding: UTF-8 -*-

import urllib3
import threading
import json
import os
from bs4 import BeautifulSoup

"""
高匿代理Ip爬虫
"""
class ProxyIpSpider:

    url = 'http://www.xicidaili.com/nn/'
    page = 1
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    def __init__(self):
        self.url = ProxyIpSpider.url
        self.page = ProxyIpSpider.page
        self.headers = ProxyIpSpider.headers
        self.ipList = []

    def spider(self):
        if os.access('db/ip_info.json', os.F_OK):
            return True

        http = urllib3.PoolManager()
        while (self.page <= 1):
            p = self.page
            res = http.request('get', self.url + str(p), headers = self.headers)
            self.parser(res.data)
            self.page += 1

    def parser(self, html):
        if html == '':
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
        # 第一栏表头不获取
        trNodes = soup.find_all('tr')[1:]
        for trNode in trNodes:
            tdNodes = trNode.find_all('td')
            ipInfo = {
                'country': tdNodes[0].get_text(),
                'ip': tdNodes[1].string,
                'port': tdNodes[2].string,
                'server_address': tdNodes[3].get_text(),
                'is_anonymity': tdNodes[4].string,
                'protocol': tdNodes[5].string,
                'speed': tdNodes[6].get_text(),
                'connection_time': tdNodes[7].get_text(),
                'live_time': tdNodes[8].string,
                'verify_time': tdNodes[9].string
            }
            # 验证有效性
            try:
                # threading.Thread(target = self.detect(ipInfo))
                self.ipList.append(ipInfo)

            except Exception:
                print(ipInfo['ip'] + ' is a bad ip')


        # ipInfo列表写入文件
        fp = open('db/ip_info.json', 'w')
        json.dump(self.ipList, fp)
        return True

    def detect(self, ipInfo = {}):
        proxyHost = ipInfo['protocol'] + '://' + ipInfo['ip'] + ':' + ipInfo['port']
        http = urllib3.ProxyManager(proxyHost)
        res = http.request('get', self.url)
        if res.getcode() == 200:
            self.ipList.append(ipInfo)
            print(ipInfo['ip'] + ' is a good ip')
        else:
            print(ipInfo['ip'] + ' is a bad ip')
