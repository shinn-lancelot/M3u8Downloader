# -*- coding: utf-8 -*-

import sys
import os
import threading
import random
import string
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QApplication, QMessageBox)
from spider import m3u8Spider
from downloader import downloader

class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主要数据
        self.websiteUrl = []
        self.m3u8Url = ''
        self.m3u8List = []
        self.downloadAll = True
        # 定义输入框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(10, 10, 250, 30)
        # 定义按钮
        self.searchBtn = QPushButton('搜索', self)
        self.searchBtn.setGeometry(270, 5, 70, 45)
        self.searchBtn.clicked.connect(self.search)
        self.downloadAllBtn = QPushButton('下载全部', self)
        self.downloadAllBtn.setGeometry(270, 55, 70, 45)
        self.downloadAllBtn.clicked.connect(
            self.downloadM3u8)
        # 定义自身窗体
        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('M3u8Downloader')
        self.show()

    def search(self):
        self.websiteUrl = self.lineEdit.text()
        if self.websiteUrl == '':
            self.alertMsg('请输入网页地址')
        else:
            spiderThread = threading.Thread(target = self.spiderM3u8List())
            spiderThread.start()

    def spiderM3u8List(self):
        p = m3u8Spider.M3u8Spider(self.websiteUrl)
        if (p.createProxyIpPool()):
            proxyUrl = p.getProxyUrl()
            userAgent = p.getUserAgent()
            header = {
                'user-agent': userAgent
            }
            self.m3u8List = p.getM3u8List('', header)
            print(self.m3u8List)

    def downloadM3u8(self):
        m3u8List = []
        if self.downloadAll == True:
            m3u8List = self.m3u8List
        else:
            m3u8List.append(self.m3u8Url)

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

    def alertMsg(self, text):
        QMessageBox.information(self, '消息', text)
        sys.exit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
