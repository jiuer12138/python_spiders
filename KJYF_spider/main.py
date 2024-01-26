import random
import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog
from scrapy.crawler import CrawlerProcess
from PySide6 import QtWidgets

from KJYF_spider.spiders.KJYF import KjyfSpider
from main_window_ui import Ui_spider
from user_agent import agent
from multiprocessing import Process, Manager


def crawl(q, is_cate, ids, dir_path, images_path):
    # CrawlerProcess
    process = CrawlerProcess(settings={
        'USER_AGENT': random.choice(agent)
    })
    process.crawl(KjyfSpider, q=q, is_cate=is_cate, ids=ids, dir_path=dir_path, images_path=images_path)
    process.start()


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

    def crawl_btn_clicked(self):
        print(self.category.isChecked())
        if self.dir_path.text() == '':
            print('请选择文件路径')
        elif self.ids.text() == '':
            print("请输入id")
        else:
            self.p = Process(target=crawl, args=(
                self.q, self.category.isChecked(), self.ids.text(), self.dir_path.text(),
                self.image_dir_path.text()))
            self.p.start()
            self.log_thread.start()

    def download_image_btn_clicked(self):
        if self.dir_path.text() == '':
            print("请选择文件路径")
        elif self.image_dir_path.text() == '':
            print("请选择图片存储路径")
        else:
            print("downloading.........")
        pass

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

                # 睡眠10毫秒，否则太快会导致闪退或者显示乱码
                self.msleep(10)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
