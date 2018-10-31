# -*- coding: UTF-8 -*-

from spider import m3u8Spider
from downloader import downloader

# import requests
# import re

# url = 'http://www.haining.tv/news/folder13/2018-10-25/209213.html'
# url = 'http://www.haining.tv/m2o/livmedia.php?id=53566&colid=13'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; MI 8 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.7.997 Mobile Safari/537.36'
# }
# res = requests.get(url, headers = headers)
# print(res.text)

# options = {
#     'm3u8Url': '',
#     'saveDir': '',
#     'file': '',
#     'downloadParams': '-vcodec copy -acodec copy -absf aac_adtstoasc'
# }

# options['m3u8Url'] = 'http://vfile.haining.tv/2018/1540/4678/1712/154046781712.ssm/154046781712.m3u8'
# options['saveDir'] = 'download/'
# options['file'] = 'video.mp4'
# options['downloadParams'] = ''

# down = downloader.Download(options)
# down.download()

# 实例化爬虫
p = m3u8Spider.M3u8Spider('http://www.haining.tv/news/folder13/2018-10-25/209213.html')
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
m3u8Url = ''
saveDir = 'download/'
file = 'video.mp4'
print(m3u8List)


# # 初始化下载参数
# options = {
#     'm3u8Url': '',
#     'saveDir': '',
#     'file': '',
#     'downloadParams': '-vcodec copy -acodec copy -absf aac_adtstoasc'
# }
# options['m3u8Url'] = m3u8Url
# options['saveDir'] = saveDir
# options['file'] = file

# # 提取m3u8流，生成mp4
# down = downloader.Downloader(options)
# res = down.download()
# print(res)
