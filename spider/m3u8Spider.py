# -*- coding: UTF-8 -*-
from spider import proxyIpSpider

"""
爬取m3u8链接
"""
class M3u8Spider:

    m3u8List = []
    proxyIpList = []

    def __init__(self, url):
        self.url = url

    def createProxyIpPool(self):
        p = proxyIpSpider.ProxyIpSpider()
        p.spider()

    def getProxyIp(self):
        print('get ip')

    def getUserAgent(self):
        print('get ua')





