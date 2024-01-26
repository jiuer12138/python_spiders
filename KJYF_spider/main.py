import sys

from scrapy.crawler import CrawlerProcess
from PySide6 import QtCore, QtWidgets, QtGui

from KJYF_spider.spiders.KJYF import KjyfSpider
from main_window_ui import Ui_spider


def crawl(q, ua, is_obey):
    # CrawlerProcess
    process = CrawlerProcess(settings={
        'USER_AGENT': ua,
        'ROBOTSTXT_OBEY': is_obey
    })

    process.crawl(KjyfSpider, q=q)
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

    def crawl_btn_clicked(self):
        print(self.category.isChecked())
        pass

    def download_image_btn_clicked(self):
        pass

    def dir_path_select_clicked(self):
        pass

    def image_dir_path_select_clicked(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
