# -*- coding: utf-8 -*-

import sys
import os
import threading
import random
import string
import re
from PyQt5.QtWidgets import (QListView, QWidget, QPushButton, QLineEdit, QApplication, QMessageBox)
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QIcon
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
        self.searchBtn.setGeometry(270, 10, 70, 30)
        self.searchBtn.clicked.connect(self.search)
        self.downloadAllBtn = QPushButton('下载全部', self)
        self.downloadAllBtn.setGeometry(270, 50, 70, 30)
        self.downloadAllBtn.clicked.connect(
            self.downloadM3u8)
        # 定义列表
        self.listView = QListView(self)
        self.listView.setGeometry(10, 50, 250, 140)
        # 定义自身窗体
        self.setGeometry(300, 300, 350, 200)
        self.setWindowIcon(QIcon('./asset/img/logo.png'))
        self.setWindowTitle('M3u8Downloader')
        self.setFixedSize(self.width(), self.height())
        self.show()

    def search(self):
        self.websiteUrl = self.lineEdit.text().strip()
        if self.websiteUrl == '':
            self.alertMsg('请输入网页地址')
        elif re.match(r'^http[s]?:/{2}\w.+$', self.websiteUrl) is None:
            self.alertMsg('请输入合法的网页地址')
        elif re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.m3u8', self.websiteUrl) is not None:
            self.m3u8List.append(self.websiteUrl)
            if len(self.m3u8List):
                stringListModel = QStringListModel()
                stringListModel.setStringList(self.m3u8List)
                self.listView.setModel(stringListModel)
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
            if len(self.m3u8List):
                stringListModel = QStringListModel()
                stringListModel.setStringList(self.m3u8List)
                self.listView.setModel(stringListModel)


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
        else:
            self.alertMsg('目前暂无可下载的m3u8地址')

    def alertMsg(self, text):
        QMessageBox.information(self, '消息', text)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
