# -*- coding: UTF-8 -*-

import requests
import urllib3
import threading
import json
import os
from bs4 import BeautifulSoup

class IpSpider:
    url = 'http://www.xicidaili.com/nn/'
    page = 1
    maxPage = 10
    checkUrl = 'https://www.ip.cn/'
    needIpNum = 10
    ipNum = 0
    filePath = 'db/'
    fileName = 'ip_info.json'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    def __init__(self):
        self.url = IpSpider.url
        self.page = IpSpider.page
        self.maxPage = IpSpider.maxPage
        self.checkUrl = IpSpider.checkUrl
        self.needIpNum = IpSpider.needIpNum
        self.ipNum = IpSpider.ipNum
        self.filePath = IpSpider.filePath
        self.fileName = IpSpider.fileName
        self.headers = IpSpider.headers
        self.ipInfoList = []

    def spider(self):
        # 判断ip信息是否存在及可用ip数量
        if os.access(self.filePath + self.fileName, os.F_OK):
            fp = open(self.filePath + self.fileName, encoding='utf-8')
            self.ipInfoList = json.load(fp)
            fp.close()
            self.ipNum = len(self.ipInfoList)
            if (self.ipNum >= self.needIpNum):
                return True

        # 爬取工作
        http = urllib3.PoolManager()
        while (self.ipNum < self.needIpNum and self.page <= self.maxPage):
            p = self.page
            res = http.request('get', self.url + str(p), headers=self.headers)
            # 解析爬取结果
            self.parser(res.data)
            self.page += 1

        # ipInfoList列表写入文件
        with open(self.filePath + self.fileName, 'w') as f:
            json.dump(self.ipInfoList, f)
        return True

    def parser(self, html):
        if html == '':
            return
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        # 第一栏表头不获取
        trNodes = soup.find_all('tr')[1:]
        for trNode in trNodes:
            if (self.ipNum >= self.needIpNum):
                break
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
                has = False
                for info in self.ipInfoList:
                    if ipInfo['ip'] == info['ip']:
                        has = True
                        break
                if has is False:
                    threading.Thread(target=self.detect(ipInfo))
            except Exception:
                print(ipInfo['ip'] + ' is a bad ip')

        return

    def detect(self, ipInfo={}):
        proxies = {
            'http': 'http://' + ipInfo['ip'] + ':' + ipInfo['port'],
            'https': 'https://' + ipInfo['ip'] + ':' + ipInfo['port']
        }
        try:
            requests.get(self.checkUrl, headers=self.headers, proxies=proxies, timeout=3)
        except:
            print(ipInfo['ip'] + ' is a good ip')
            self.ipInfoList.append(ipInfo)
            self.ipNum += 1
        else:
            print(ipInfo['ip'] + ' is a bad ip')
        return
