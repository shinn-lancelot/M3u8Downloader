# -*- coding: UTF-8 -*-

import random
import string
from spider import m3u8Spider
from downloader import downloader
from sys import argv

# example:python3 main http://www.jiaxingren.com/folder24/folder147/folder149/folder170/2018-10-25/416269.html

websiteUrl = ''
if len(argv) < 2:
    exit('请输入要网页地址')
else:
    websiteUrl = argv[1]

if websiteUrl == '':
    exit('请输入要网页地址')

# 实例化爬虫
p = m3u8Spider.M3u8Spider(websiteUrl)
# 创建代理ip池
# p.createProxyIpPool()
# 生成代理地址
proxyUrl = p.getProxyUrl()
# 生成用户代理
userAgent = p.getUserAgent()
header = {
    'user-agent': userAgent
}
# 获取m3u8di地址列表
m3u8List = p.getM3u8List(proxyUrl, header)
print(m3u8List)

if len(m3u8List) > 0:
    saveDir = 'download/'
    file = 'video.mp4'
    # 初始化下载参数
    options = {
        'm3u8Url': '',
        'saveDir': saveDir,
        'file': file,
        'downloadParams': '-vcodec copy -acodec copy -absf aac_adtstoasc'
    }
    for m3u8Url in m3u8List:
        options['m3u8Url'] = m3u8Url
        options['file'] = ''.join(random.sample(
            string.ascii_letters + string.digits, 16)) + '.mp4'

        # 提取m3u8流，生成mp4
        down = downloader.Downloader(options)
        res = down.download()
        print(res)
