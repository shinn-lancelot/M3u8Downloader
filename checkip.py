# -*- coding: UTF-8 -*-

import threading
import json
import random
import urllib3


def detect(ipList=[]):
    for ipInfo in ipList:
        try:
            proxyHost = ipInfo['protocol'] + '://' + ipInfo['ip'] + ':' + ipInfo['port']
            http = urllib3.ProxyManager(proxyHost)
            targetUrl = 'http://www.xicidaili.com/nn/'
            res = http.request('get', targetUrl, timeout=urllib3.Timeout(connect=3.0, read=1.0))
            if res.getcode() == 200:
                print(ipInfo['ip'] + ' is a good ip')
            else:
                print(ipInfo['ip'] + ' is a bad ip')
        except:
            print(ipInfo['ip'] + ' is a bad ip')

ipInfo = []
fp = open('db/ip_info.json', encoding='utf-8')
ipInfolist = json.load(fp)
fp.close()

thNum = 10
listNum = int(len(ipInfolist) / thNum)
newList = []

print('ip总数：{}'.format(len(ipInfolist)))
print('线程总数：{}'.format(thNum))
print('单线程处理ip总数：{}'.format(listNum))

for ipInfo in ipInfolist:
    newList.append(ipInfo)
    if len(newList) >= listNum:
        print(len(newList))
        print('==========')
        th = threading.Thread(target=detect, args=(newList,))
        th.start()
        newList = []
