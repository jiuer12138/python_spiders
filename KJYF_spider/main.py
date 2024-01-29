import random
import sys

from PySide6.QtCore import QThread
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog
from openpyxl import load_workbook
from scrapy.crawler import CrawlerProcess
from PySide6 import QtWidgets

from KJYF_spider.spiders.KJYF import KjyfSpider
from main_window_ui import Ui_spider
from multiprocessing import Process, Manager
from KJYF_spider.utils import format_str
from scrapy.utils.project import get_project_settings
import urllib.request

settings = get_project_settings()


def crawl(q, is_cate, ids, dir_path):
    # CrawlerProcess
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(KjyfSpider, q=q, is_cate=is_cate, ids=ids, dir_path=dir_path)
    process.start()

    # 下载图片


def get_image_urls(q1, path, image_dir_path):
    q1.put(format_str('开始下载图片'))
    wb = load_workbook(path + '/' + settings.get('CUSTOM_EXECL_FILE_NAME'))
    # 获取活动工作表
    sheet = wb['Sheet']
    #  获取第一行表头
    col = None
    p_id_col = None
    # 第一行
    rows = list(sheet.rows)[0]
    for i in range(len(rows)):
        if '图片' in list(sheet.rows)[0][i].value:
            col = i
        if '产品id' in list(sheet.rows)[0][i].value:
            p_id_col = i
    if col is None:
        q1.put(format_str('表格中没有包含图片列'))
    p_id_cols = []
    for p_id in list(sheet.columns)[p_id_col]:
        p_id_cols.append(p_id.value)
    print(p_id_cols)
    target = list(sheet.columns)[col]
    for j in range(1, len(target)):
        if target[j].value:
            urls = target[j].value.split(',')
            for x in range(len(urls)):
                print('=======')
                print(p_id_cols[j])
                q1.put(format_str('正在下载：' + urls[x]))
                suffix = urls[x].rsplit('.', 1)[-1]
                urllib.request.urlretrieve(urls[x],
                                           image_dir_path + '/' + str(p_id_cols[j]) + '_' + str(
                                               x + 1) + '.' + suffix)
            q1.put(format_str('产品id为：' + str(p_id_cols[j]) + '共' + str(len(urls)) + '张图片下载完成'))
    q1.put(format_str('所有图片下载完成'))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_spider()
        self.ui.setupUi(self)
        # 文件路径
        self.dir_path = self.ui.dir_path
        # 文件路径选择
        self.dir_path_select = self.ui.dir_path_select
        #  当前输入的是分类id或者产品id
        self.category = self.ui.category
        self.product = self.ui.product
        # 分类id
        self.ids = self.ui.ids
        # 图片存储路径
        self.image_dir_path = self.ui.image_dir_path
        # 图片存储路径选择
        self.image_dir_path_select = self.ui.image_dir_path_select
        # 日志输出
        self.logs_output = self.ui.logs_output
        # 开启爬虫爬取
        self.crawl_btn = self.ui.crawl_btn
        # 开启下载图片
        self.download_image_btn = self.ui.download_image_btn

        # 连接信号
        self.crawl_btn.clicked.connect(self.crawl_btn_clicked)
        self.download_image_btn.clicked.connect(self.download_image_btn_clicked)
        self.dir_path_select.clicked.connect(self.dir_path_select_clicked)
        self.image_dir_path_select.clicked.connect(self.image_dir_path_select_clicked)

        # 默认初始分类id
        self.category.setChecked(True)
        # 创建线程
        self.q = Manager().Queue()
        self.log_thread = LogThread(self)
        self.p = None
        self.p1 = None

        #  日志输出滚动条自动滚到最下方
        self.logs_output.textChanged.connect(self.logs_output.moveCursor(QTextCursor.End))

    def crawl_btn_clicked(self):
        if self.dir_path.text() == '':
            self.logs_output.append(format_str("请选择文件存储路径"))
        elif self.ids.text() == '':
            self.logs_output.append(format_str("请输入id"))
        else:
            self.p = Process(target=crawl, args=(
                self.q, self.category.isChecked(), self.ids.text(), self.dir_path.text()))
            self.p.start()
            self.log_thread.start()

    def download_image_btn_clicked(self):
        if self.dir_path.text() == '':
            self.logs_output.append(format_str("请选择文件路径"))
        elif self.image_dir_path.text() == '':
            self.logs_output.append(format_str("请选择图片存储路径"))
        else:
            self.p1 = Process(target=get_image_urls, args=(self.q, self.dir_path.text(), self.image_dir_path.text()))
            self.p1.start()
            self.log_thread.start()

    def dir_path_select_clicked(self):
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", './')
        if file_path:
            self.dir_path.setText(file_path)

    def image_dir_path_select_clicked(self):
        file_path = QFileDialog.getExistingDirectory(self, "Select Directory", './')
        if file_path:
            self.image_dir_path.setText(file_path)


class LogThread(QThread):
    def __init__(self, gui):
        super(LogThread, self).__init__()
        self.gui = gui

    def run(self):
        while True:
            if not self.gui.q.empty():
                self.gui.logs_output.append(self.gui.q.get())
                # # 确保滑动条到底
                # cursor = self.gui.logs_output.textCursor()
                # pos = len(self.gui.logs_output.toPlainText())
                # cursor.movePosition(pos)
                # self.gui.logs_output.setTextCursor(cursor)
                # if '爬取结束' in self.gui.logs_output.toPlainText():
                #     self.gui.crawl_btn.setText('开始爬取')
                #     break
                # 睡眠10毫秒，否则太快会导致闪退或者显示乱码
                self.msleep(10)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
