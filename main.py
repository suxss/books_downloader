# -*- coding: UTF-8 -*-
import os
import random
import threading
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QIcon
import requests
import LanZou
from CtCloud import CtCloud
from untitled import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QStyleFactory, QMenu
from PyQt5 import QtCore
import json
import YouDao
import DouBan
import YuQue
import logging
import time
from Bloogle import Bloogle
from KgBook import KgBook
from kindle8 import Kindle8
from KsMao import KsMao
from LanJuHua import LanJuHua
from mnbooks import MNBooks
from pdfZiYuan import pdfZY
from QiLiXiang import QiLiXiang
from SoBooks import SoBooks
from SuiJi import SuiJi
from NewDownloader import Download


def read_top250():
    with open('top250.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
    return d


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


class TranslateThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(TranslateThread, self).__init__()

    def run(self):
        try:
            result = YouDao.translate(word=self.word)
        except:
            result = ''
        self.signal.emit(result)


class Top250UpdateThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(Top250UpdateThread, self).__init__()

    def run(self):
        douban = DouBan.DouBan()
        douban.get_top_250()
        self.signal.emit('更新完成！内容在重启软件后刷新。')


class SearchThread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, code1, code2, proxy):
        super(SearchThread, self).__init__()
        self.Sobooks_code = code1
        self.kindle8_code = code2
        self.proxy = proxy

        try:
            if self.source == "SoBooks":
                sobooks = SoBooks(proxy=self.proxy)
                sobooks.code = self.Sobooks_code
                result = sobooks.search(self.word, page=self.page)  # {'name':[],'author':[],'url':[]}
            elif self.source == "Bloogle":
                bloogle = Bloogle(proxy=self.proxy)
                result = bloogle.search(self.word, page=self.page)  # {'name':[],'url':[]}
            elif self.source == "KgBook":
                kgbook = KgBook(proxy=self.proxy)
                result = kgbook.search(self.word, page=self.page)  # {'name':[],'url':[]}
            elif self.source == "kindle8":
                kindle8 = Kindle8(proxy=self.proxy)
                kindle8.code = self.kindle8_code
                result = kindle8.search(self.word, page=self.page)  # {'name':[],'url':[]}
            elif self.source == "KsMao":
                ksmao = KsMao(proxy=self.proxy)
                result = ksmao.search(self.word)  # {'name':[],'url':[],'host': []}
            elif self.source == "LanJuHua":
                lanjuhua = LanJuHua(proxy=self.proxy)
                result = lanjuhua.search(self.word, page=self.page)  # {'name':[],'fid':[]}
            elif self.source == "mnbooks":
                mnbooks = MNBooks(proxy=self.proxy)
                result = mnbooks.search(self.word, page=self.page)  # {'name':[],'url':[]}
            elif self.source == "pdfZiYuan":
                pdfzy = pdfZY(proxy=self.proxy)
                result = pdfzy.search(self.word, page=self.page)  # {'name':[],'url':[]}
            elif self.source == "SuiJi":
                suiji = SuiJi(proxy=self.proxy)
                result = suiji.search(self.word)  # {'name':[],'url':[]}
            else:  # self.source == "QiLiXiang":
                qilixiang = QiLiXiang(proxy=self.proxy)
                result = qilixiang.search(word=self.word, page=self.page)  # {'name':[],'author':[],'url':[]}
        except:
            result = {'name': [], 'url': []}
        self.signal.emit(result)


class DownloadThread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, code1, code2, proxy=None):
        super(DownloadThread, self).__init__()
        self.Sobooks_code = code1
        self.kindle8_code = code2
        self.proxy = proxy

    def run(self):
        result = {'error': 0, 'row': self.n}
        name = None
        try:
            if self.source == "SoBooks":
                sobooks = SoBooks(proxy=self.proxy)
                sobooks.code = self.Sobooks_code
                dic = sobooks.get_book_link(self.search_result['url'][self.n])
                if dic['platform'] == 'ct':
                    ctcloud = CtCloud()
                    down_link = ctcloud.get_dow_url(dic['url'])
                elif dic['platform'] == 'lz':
                    link_1 = LanZou.put_passcode(dic['url'], dic['password'])
                    down_link = LanZou.get_file_info(link_1)  # {'name':[],'author':[],'url':[]}
            elif self.source == "Bloogle":
                bloogle = Bloogle(proxy=self.proxy)
                down_link = bloogle.get_down_url(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            elif self.source == "KgBook":
                kgbook = KgBook(proxy=self.proxy)
                down_link = kgbook.get_down_link(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            elif self.source == "kindle8":
                kindle8 = Kindle8(proxy=self.proxy)
                kindle8.code = self.kindle8_code
                down_link = kindle8.get_down_link(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            elif self.source == "KsMao":
                ksmao = KsMao(proxy=self.proxy)
                down_link = ksmao.get_down_link(self.search_result['url'][self.n],
                                                self.search_result['host'][self.n])  # {'name':[],'url':[],'host': []}
            elif self.source == "LanJuHua":
                lanjuhua = LanJuHua(proxy=self.proxy)
                down_link = lanjuhua.get_dow_link(self.search_result['fid'][self.n])  # {'name':[],'fid':[]}
            elif self.source == "mnbooks":
                mnbooks = MNBooks(proxy=self.proxy)
                down_link = mnbooks.get_dow_link(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            elif self.source == "pdfZiYuan":
                pdfzy = pdfZY(proxy=self.proxy)
                down_link = pdfzy.get_dow_link(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            elif self.source == "SuiJi":
                suiji = SuiJi(proxy=self.proxy)
                down_link = suiji.get_dow_link(self.search_result['url'][self.n])  # {'name':[],'url':[]}
            else:  # self.source == "QiLiXiang":
                down_link = self.search_result['url'][self.n]
            downloader = Download(down_link,
                                  file_dir=self.save_dir,
                                  file_name=name,
                                  name_mode=(2 if name else 1),
                                  thread_num=int(self.threads))
            downloader.download()
        except Exception as e:
            logging.error(f'Downloader error: {e}\n\tSource:{self.source}\n\tUrl:{self.search_result["fid"][self.n] if self.source == "LanJuHua" else self.search_result["url"][self.n]}')
            result['error'] = 1
        self.signal.emit(result)


class NewVersionThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(NewVersionThread, self).__init__()

    def run(self):
        downloader = Download(self.url, file_dir='./新版本/', file_name=self.version, name_mode=2, thread_num=int(self.threads))
        downloader.download()
        self.signal.emit('更新完毕')


class CleanLogsThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(CleanLogsThread, self).__init__()

    def run(self):
        clean_log('./Logs/')
        self.signal.emit('清理完毕')


class Demo(QMainWindow, Ui_MainWindow):
    version = "1.0"  # 版本号

    def __init__(self):
        super(Demo, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyle(QStyleFactory.create("Window"))
        self.setWindowIcon(QIcon('./image/favicon.ico'))

        # 将右键菜单绑定到槽函数generateMenu
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

        # 翻译线程
        self.translate_thread = TranslateThread()
        self.translate_thread.signal.connect(self.textBrowser_2.setText)
        # Top250更新线程
        self.top250_update_thread = Top250UpdateThread()
        self.top250_update_thread.signal.connect(self.messagebox)
        # 清理日志线程
        self.clean_logs_thread = CleanLogsThread()
        self.clean_logs_thread.signal.connect(self.messagebox)
        # 下载新版本线程
        self.new_version_thread = NewVersionThread()
        self.new_version_thread.signal.connect(self.messagebox)

        self.pushButton_7.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.showMinimized)
        self.pushButton.clicked.connect(lambda: self.btn_change_index(0))
        self.pushButton_2.clicked.connect(lambda: self.btn_change_index(1))
        self.pushButton_3.clicked.connect(lambda: self.btn_change_index(2))
        self.pushButton_4.clicked.connect(lambda: self.btn_change_index(3))
        self.pushButton_22.clicked.connect(lambda: self.btn_change_index(4))
        self.pushButton_10.clicked.connect(lambda: self.change_top250_page(1))
        self.pushButton_11.clicked.connect(lambda: self.change_top250_page(-1))
        self.pushButton_5.clicked.connect(self.last_widget)
        self.pushButton_23.clicked.connect(self.translate)
        self.pushButton_28.clicked.connect(self.top250_updata)
        self.pushButton_24.clicked.connect(self.choose_save_dir)
        self.pushButton_25.clicked.connect(self.restore_config)
        self.pushButton_27.clicked.connect(self.save_config)
        self.pushButton_29.clicked.connect(self.clean_logs)
        self.pushButton_26.clicked.connect(self.search)
        self.pushButton_9.clicked.connect(self.next_search_page)
        self.pushButton_8.clicked.connect(self.last_search_page)
        self.pushButton_30.clicked.connect(self.about)

        self.current_search_result = None
        self.current_source = None
        self.current_search_word = None
        self.index_record = [0]
        self.initialize()



        # 搜索线程
        self.search_thread = SearchThread(proxy=self.proxy, code1=self.new_info['Code']['SoBooks'],
                                          code2=self.new_info['Code']['kindle8'])
        self.search_thread.signal.connect(self.show_search_result)

        self.top250_search_initialize()


    def initialize(self):
        self.comboBox.clear()
        self.current_search_page = 1
        self.proxy = None
        self.top_page = 0
        self.top250_initialize()
        self.last_widget_index = 0
        self.current_widget_index = 0
        self.settings = QtCore.QSettings("config.ini", QtCore.QSettings.IniFormat)
        self.read_config()
        self.new_info = YuQue.get_info(proxy=self.proxy)
        if self.settings.value('FIRST') == 'True':
            self.read_config_form_yuque()
            self.settings.setValue('FIRST', 'False')
        else:
            self.settings_initialize()

    def events_after_show(self):
        if self.check_new_version:
            self.Check_New_Version()
        self.compare_two_config()
        self.announce()

    def settings_initialize(self):
        checkbox = tuple([f'_{i}' for i in range(2, 12)])
        name = [('QiLiXiang', '七里香'), ('SoBooks', 'SoBooks'), ('KgBook', '苦瓜书盘'), ('kindle8', 'kindle吧'),
                ('KsMao', '快搜猫'),
                ('mnbooks', '码农书籍网'), ('SuiJi', '随机阅读'), ('LanJuHua', '蓝菊花搜索'), ('Bloogle', 'Bloogle'),
                ('pdfZiYuan', 'pdf资源网')]
        for i in range(10):
            if not eval(f'self.{name[i][0]}'):
                exec(f'self.checkBox{checkbox[i]}.setCheckState(QtCore.Qt.Unchecked)')
            else:
                exec(f'self.checkBox{checkbox[i]}.setCheckState(QtCore.Qt.Checked)')
                self.comboBox.addItem(name[i][1])
        if not self.check_new_version:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        self.lineEdit_2.setText(self.save_dir)
        if self.proxy and self.proxy.strip():
            self.lineEdit_3.setText(self.proxy)
        if self.threads in ['1', '2', '4']:
            self.comboBox_2.setCurrentIndex(['1', '2', '4'].index(self.threads))

    def top250_search_initialize(self):
        self.pushButton_12.clicked.connect(lambda: self.quick_search(0))
        self.pushButton_13.clicked.connect(lambda: self.quick_search(1))
        self.pushButton_14.clicked.connect(lambda: self.quick_search(2))
        self.pushButton_15.clicked.connect(lambda: self.quick_search(3))
        self.pushButton_16.clicked.connect(lambda: self.quick_search(4))
        self.pushButton_19.clicked.connect(lambda: self.quick_search(5))
        self.pushButton_18.clicked.connect(lambda: self.quick_search(6))
        self.pushButton_21.clicked.connect(lambda: self.quick_search(7))
        self.pushButton_17.clicked.connect(lambda: self.quick_search(8))
        self.pushButton_20.clicked.connect(lambda: self.quick_search(9))

    def top250_initialize(self):
        self.top250_dict = read_top250()
        pic_label = ('', '_3', '_4', '_5', '_7', '_10', '_11', '_8', '_14', '_13')
        name_label = ('_12', '_13', '_14', '_15', '_16', '_19', '_18', '_21', '_17', '_20')
        num_label = ('_2', '_6', '_9', '_12', '_15', '_20', '_19', '_16', '_17', '_18')
        for i in range(len(pic_label)):
            try:
                exec(
                    f"self.label{pic_label[i]}.setPixmap(QtGui.QPixmap.fromImage(QImage.fromData(requests.get(self.top250_dict['pic'][{self.top_page * 10 + i}],headers={{'Accept-Encoding': 'gzip, deflate'}}).content)))")
            except Exception as e:
                logging.warning(f"Request error {e} > {self.top250_dict['pic'][self.top_page * 10 + i]}  Retry")
                exec(
                    f"self.label{pic_label[i]}.setPixmap(QtGui.QPixmap.fromImage(QImage.fromData(requests.get(self.top250_dict['pic'][{self.top_page * 10 + i}],headers={{'Accept-Encoding': 'gzip, deflate'}}).content)))")
            exec(
                f"self.pushButton{name_label[i]}.setText(QtCore.QCoreApplication.translate('MainWindow', self.top250_dict['name'][{self.top_page * 10 + i}][:8]))")
            exec(
                f"self.label{num_label[i]}.setText(QtCore.QCoreApplication.translate('MainWindow', '{self.top_page * 10 + i + 1}.'))")

    def change_widget(self, index):
        buttons = ('', '_2', '_3', '_4', '_22')
        white_icons = (
            ':/icon/icon_hawtduws6br/shu.png',
            ':/icon/icon_hawtduws6br/sousuo.png',
            ':/icon/icon_hawtduws6br/xiazai.png',
            ':/icon/icon_hawtduws6br/翻译 (1).png',
            ':/icon/icon_hawtduws6br/shezhi.png')
        green_icons = (
            ':/icon/icon_ozaegulmxh/shu.png',
            ':/icon/icon_ozaegulmxh/sousuo.png',
            ':/icon/icon_ozaegulmxh/xiazai.png',
            ':/icon/icon_ozaegulmxh/翻译.png',
            ':/icon/icon_ozaegulmxh/shezhi.png')
        self.stackedWidget.setCurrentIndex(index)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(white_icons[self.current_widget_index]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        exec(f"self.pushButton{buttons[self.current_widget_index]}.setIcon(icon)")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(green_icons[index]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        exec(f"self.pushButton{buttons[index]}.setIcon(icon1)")
        self.last_widget_index = self.current_widget_index
        self.current_widget_index = index

    def change_top250_page(self, n):
        if 0 <= self.top_page + n <= 25:
            self.top_page += n
            try:
                MyThread(self.top250_initialize)
            except Exception as e:
                print(e)

    def btn_change_index(self, index):
        if index != self.current_widget_index:
            self.change_widget(index)
            self.index_record.append(index)

    def last_widget(self):
        self.change_widget(self.last_widget_index)
        if len(self.index_record) > 1:
            self.index_record.pop()
            if len(self.index_record) > 1:
                self.current_widget_index = self.index_record[-1]
                self.last_widget_index = self.index_record[-2]
            else:
                self.current_widget_index = self.index_record[-1]
                self.last_widget_index = self.index_record[-1]

    def quick_search(self, i):
        word = self.top250_dict['name'][self.top_page * 10 + i]
        self.lineEdit.setText(word)
        self.pushButton_26.click()

    def search(self, word=None, page=None):
        name = {'SoBooks': 'SoBooks', '苦瓜书盘': 'KgBook', 'kindle吧': 'kindle8', '快搜猫': 'KsMao', '码农书籍网': 'mnbooks',
                '随机阅读': 'SuiJi', '蓝菊花搜索': 'LanJuHua', 'Bloogle': 'Bloogle', 'pdf资源网': 'pdfZiYuan', '七里香': 'QiLiXiang'}
        if not word and self.lineEdit.text().strip():
            self.current_search_word = self.lineEdit.text().strip()
        if not page:
            page = 1
            self.label_24.setText("第 1 页")
        self.current_source = self.search_thread.source = name[self.comboBox.currentText()]
        self.current_search_page = self.search_thread.page = page
        self.search_thread.word = self.current_search_word
        self.search_thread.start()

    def next_search_page(self):
        if self.current_source and self.current_search_word and self.current_source not in {'KsMao', 'SuiJi'}:
            self.current_search_page += 1
            self.search(word=self.current_search_word, page=self.current_search_page)
            self.label_24.setText(f'第 {self.current_search_page} 页')

    def last_search_page(self):
        if self.current_source and self.current_search_word and self.current_source not in {'KsMao',
                                                                                            'SuiJi'} and self.current_search_page > 1:
            self.current_search_page -= 1
            self.search(word=self.current_search_word, page=self.current_search_page)
            self.label_24.setText(f'第 {self.current_search_page} 页')

    def show_search_result(self, search_result):
        self.current_search_result = search_result

        for _ in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)

        if 1 != self.current_widget_index:
            self.change_widget(1)
            self.index_record.append(1)

        if 'author' not in search_result:
            for i in range(len(search_result['name'])):
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(
                    QtCore.QCoreApplication.translate(
                        "MainWindow", search_result['name'][i])))
        else:
            for i in range(len(search_result['name'])):
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(
                    QtCore.QCoreApplication.translate(
                        "MainWindow", search_result['name'][i])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(
                    QtCore.QCoreApplication.translate(
                        "MainWindow", search_result['author'][i])))

    def download_books(self, n):
        name = self.current_search_result['name'][n]
        i = self.tableWidget_2.currentRow() + 1
        self.tableWidget_2.insertRow(i)
        self.tableWidget_2.setItem(i, 0, QTableWidgetItem(
            QtCore.QCoreApplication.translate(
                "MainWindow", name)))
        self.tableWidget_2.setItem(i, 1, QTableWidgetItem(
            QtCore.QCoreApplication.translate(
                "MainWindow", '下载中')))
        r = random.randint(100, 999)
        exec(f"self.downloader_{r} = DownloadThread(proxy=self.proxy, code1=self.new_info['Code']['SoBooks'], code2=self.new_info['Code']['kindle8'])")
        eval(f"self.downloader_{r}").signal.connect(self.down_finish)
        eval(f"self.downloader_{r}").search_result = self.current_search_result
        eval(f"self.downloader_{r}").n = n
        eval(f"self.downloader_{r}").row = i
        eval(f"self.downloader_{r}").source = self.current_source
        eval(f"self.downloader_{r}").save_dir = self.save_dir
        eval(f"self.downloader_{r}").threads = self.threads
        eval(f"self.downloader_{r}").start()

    def down_finish(self,result_dict):
        if not result_dict['error']:
            self.tableWidget_2.setItem(result_dict['row'], 1, QTableWidgetItem(
                QtCore.QCoreApplication.translate(
                    "MainWindow", '下载完毕')))
        else:
            self.tableWidget_2.setItem(result_dict['row'], 1, QTableWidgetItem(
                QtCore.QCoreApplication.translate(
                    "MainWindow", '下载失败')))

    def translate(self, word=None):
        if word:
            self.change_widget(3)
            self.index_record.append(3)
            self.translate_thread.word = word
            self.textBrowser.setPlainText(word)
            self.translate_thread.start()
        elif not word and self.textBrowser.toPlainText():
            self.translate_thread.word = self.textBrowser.toPlainText()
            self.translate_thread.start()

    def top250_updata(self):
        self.top250_update_thread.start()

    def messagebox(self, content, title='消息'):
        QMessageBox.information(self, title, content, QMessageBox.Ok, QMessageBox.Ok)

    def choose_save_dir(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选取文件夹')
        self.lineEdit_2.setText(dir_choose)

    def set_current_source(self):
        dict_1 = {'Soboks': 'SoBooks', '苦瓜书盘': 'KgBook', 'kindle吧': 'kindle8', '快搜猫': 'KsMao', '码农书籍网': 'mnbooks',
                  '随机阅读': 'SuiJi', '蓝菊花搜索': 'LanJuHua', 'Bloogle': 'Bloogle', 'pdf资源网': 'pdfZiYuan', '七里香': 'QiLiXiang'}
        self.current_source = dict_1[self.comboBox.currentText()]

    def update_combox(self):
        name1 = (
            'QiLiXiang', 'SoBooks', 'KgBook', 'kindle8', 'KsMao', 'mnbooks', 'SuiJi', 'LanJuHua', 'Bloogle', 'pdfZiYuan'
        )
        name2 = ('七里香', 'SoBooks', '苦瓜书盘', 'kindle吧', '快搜猫', '码农书籍网', '随机阅读', '蓝菊花搜索', 'Bloogle', 'pdf资源网')
        self.comboBox.clear()
        for i in range(10):
            if eval(f'self.{name1[i]}'):
                self.comboBox.addItem(name2[i])

    def announce(self):
        if self.new_info['Message'].strip():
            self.messagebox(self.new_info['Message'].strip(), title='公告')

    def read_config_form_yuque(self):
        name = (
            'SoBooks', 'KgBook', 'kindle8', 'KsMao', 'mnbooks', 'SuiJi', 'LanJuHua', 'Bloogle', 'pdfZiYuan',
            'QiLiXiang')
        for item in name:
            exec(f"self.{item} = (self.new_info['State'][item] == 'On')")

    def read_config(self):
        self.save_dir = self.settings.value('SAVE_DIR')  # 下载保存路径
        self.proxy = self.settings.value('PROXY')  # 代理ip
        if self.proxy == 'None':
            self.proxy = None
        self.threads = self.settings.value('THREADS')  # 默认线程数
        self.check_new_version = (self.settings.value('CHECK_NEW_VERSION') == 'ON')  # 自动检测新版本
        self.SoBooks = (self.settings.value('STATE/SOBOOKS') == 'ON')
        self.KgBook = (self.settings.value('STATE/KGBOOK') == 'ON')
        self.kindle8 = (self.settings.value('STATE/KINDLE8') == 'ON')
        self.KsMao = (self.settings.value('STATE/KSMAO') == 'ON')
        self.mnbooks = (self.settings.value('STATE/MNBOOKS') == 'ON')
        self.SuiJi = (self.settings.value('STATE/SUIJI') == 'ON')
        self.LanJuHua = (self.settings.value('STATE/LANJUHUA') == 'ON')
        self.Bloogle = (self.settings.value('STATE/BLOOGLE') == 'ON')
        self.pdfZiYuan = (self.settings.value('STATE/PDFZIYUAN') == 'ON')
        self.QiLiXiang = (self.settings.value('STATE/QILIXIANG') == 'ON')

    def compare_two_config(self):
        name = {'SoBooks': 'SoBooks', 'KgBook': '苦瓜书盘', 'kindle8': 'kindle吧', 'KsMao': '快搜猫', 'mnbooks': '码农书籍网',
                'SuiJi': '随机阅读', 'LanJuHua': '蓝菊花搜索', 'Bloogle': 'Bloogle', 'pdfZiYuan': 'pdf资源网',
                'QiLiXiang': '七里香'}
        un_equal = []
        for item in name.keys():
            if self.new_info['State'][item].lower() != self.settings.value('STATE/' + item.upper()).lower() and \
                    self.new_info['State'][item].lower() != 'on':
                un_equal.append(name[item])
        if len(un_equal) > 0:
            self.messagebox(f'书源:{", ".join(un_equal)}已失效，建议在设置中将其关闭')

    def restore_config(self):  # 恢复默认设置
        self.lineEdit_3.setText('')
        self.read_config_form_yuque()
        self.save_dir = './books/'
        self.threads = '1'
        self.check_new_version = True
        self.proxy = None
        self.settings.setValue('FIRST', 'True')
        self.settings_initialize()
        self.save_config()

    def save_config(self):
        checkbox = tuple([f'_{i}' for i in range(2, 12)])
        name = (
            'SoBooks', 'KgBook', 'kindle8', 'KsMao', 'mnbooks', 'SuiJi', 'LanJuHua', 'Bloogle', 'pdfZiYuan',
            'QiLiXiang')
        for i in range(10):
            exec(f"self.{name[i]} = self.checkBox{checkbox[i]}.isChecked()")
        self.check_new_version = self.checkBox.isChecked()
        self.save_dir = self.lineEdit_2.text()
        if self.lineEdit_3.text().strip():
            self.proxy = self.lineEdit_3.text().strip()
        else:
            self.proxy = None
        self.threads = self.comboBox_2.currentText()

        for item in name:
            self.settings.setValue('STATE/' + item.upper(), 'ON' if eval(f'self.{item}') else 'OFF')
        name2 = ('save_dir', 'threads')
        for item in name2:
            self.settings.setValue(item.upper(), eval(f'self.{item}'))
        if self.proxy:
            self.settings.setValue('PROXY', self.proxy)
        else:
            self.settings.setValue('PROXY', 'None')
        self.settings.setValue('CHECK_NEW_VERSION', 'ON' if self.check_new_version else 'OFF')
        self.update_combox()
        self.messagebox('保存成功')

    def Check_New_Version(self):
        if self.version != self.new_info['Version']:
            a = QMessageBox.question(self, "版本更新", "存在新版本，是否更新？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if a == QMessageBox.Yes:
                self.download_new_version()

    def download_new_version(self):
        if self.new_info['DownloadUrl'].strip():
            self.new_version_thread.url = self.new_info['DownloadUrl'].strip()
            self.new_version_thread.threads = self.threads
            self.new_version_thread.version = self.new_info['Version']
            self.new_version_thread.start()
        else:
            logging.warning('New version download url is none!')

    def clean_logs(self):
        self.clean_logs_thread.start()

    def about(self):
        url = 'https://github.com/SuXss/books_downloader'
        self.messagebox(f"版本:  {self.version}\n开源地址: {url}", title='关于')

    def generateMenu(self, pos):
        menu = QMenu()
        item1 = menu.addAction(u'下载')
        item2 = menu.addAction(u'翻译')
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == item1:
            self.download_books(self.tableWidget.currentRow())

        elif action == item2:
            self.translate(self.tableWidget.currentItem().text())

    def mousePressEvent(self, event):  # 鼠标长按事件
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标移动事件
        try:
            if QtCore.Qt.LeftButton and self.m_drag:
                self.move(QMouseEvent.globalPos() - self.m_DragPosition)
                QMouseEvent.accept()
        except AttributeError as e:
            logging.error(f'AttributeError:  {str(e)}  || Function: mouseMoveEvent')

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标释放事件
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


def strToTimestamp(time_st, format='%Y%m%d%H%M%S'):
    t = time.strptime(time_st, format)
    res = time.mktime(t)
    return res


def timestampToStr(time_strmp, format='%Y%m%d%H%M%S'):
    cur_time = time.localtime(time_strmp)
    res = time.strftime(format, cur_time)
    return res


# 清理最近三天之外的日志文件
def clean_log(path):
    if os.path.exists(path) and os.path.isdir(path):
        today = time.strftime('%Y%m%d')
        cur_timestamp = strToTimestamp(today, '%Y%m%d')
        yesterday = cur_timestamp - 86400
        before_yesterday = yesterday - 86400
        file_name_list = [today, timestampToStr(yesterday, '%Y%m%d'), timestampToStr(before_yesterday, '%Y%m%d')]
        # 求出最近三天的日期格式
        for file in os.listdir(path):
            file_name_sp = file.split('.')
            if len(file_name_sp) >= 2:
                file_date = file_name_sp[0].split('-')[1]
                if file_date not in file_name_list:
                    abs_path = os.path.join(path, file)
                    os.remove(abs_path)


def except_hook(cls, exception, ttraceback):
    sys.__excepthook__(cls, exception, ttraceback)
    mainLogger = logging.getLogger("Main")
    mainLogger.critical("Uncaught exception", exc_info=(cls, exception, ttraceback))
    sys.exit(1)


if __name__ == '__main__':
    sys.excepthook = except_hook

    log_path = './Logs/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'

    logging.basicConfig(filename=log_file_name, level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] >>>  %('
                                                                            'message)s', datefmt='%Y-%m-%d %I:%M:%S')

    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    demo.events_after_show()
    sys.exit(app.exec_())
