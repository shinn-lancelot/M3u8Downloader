# -*- coding: UTF-8 -*-

import os

"""
下载/提取m3u8视频
"""
class Downloader:
    def __init__(self, options = {}):
        self.options = options

    def download(self):
        if not os.path.exists(self.options['saveDir']):
            os.makedirs(self.options['saveDir'])

        cmd = 'ffmpeg -i "' + self.options['m3u8Url'] + '" ' + self.options['downloadParams'] + ' ' + self.options['saveDir'] + self.options['file']
        return self.exeCmd(cmd)

    def exeCmd(self, cmd):
        f = os.popen(cmd)
        text = f.read().strip()
        f.close()
        return text

