# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QTextEdit, QWidget)

class Ui_spider(object):
    def setupUi(self, spider):
        if not spider.objectName():
            spider.setObjectName(u"spider")
        spider.resize(579, 478)
        self.crawl_btn = QPushButton(spider)
        self.crawl_btn.setObjectName(u"crawl_btn")
        self.crawl_btn.setGeometry(QRect(460, 70, 113, 41))
        self.logs_label = QLabel(spider)
        self.logs_label.setObjectName(u"logs_label")
        self.logs_label.setGeometry(QRect(10, 180, 60, 16))
        self.dir_path = QLineEdit(spider)
        self.dir_path.setObjectName(u"dir_path")
        self.dir_path.setGeometry(QRect(160, 40, 281, 21))
        self.dir_path_label = QLabel(spider)
        self.dir_path_label.setObjectName(u"dir_path_label")
        self.dir_path_label.setGeometry(QRect(70, 40, 78, 18))
        self.label_5 = QLabel(spider)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(170, 100, 211, 16))
        self.download_image_btn = QPushButton(spider)
        self.download_image_btn.setObjectName(u"download_image_btn")
        self.download_image_btn.setGeometry(QRect(460, 160, 113, 41))
        self.image_dir_path_label = QLabel(spider)
        self.image_dir_path_label.setObjectName(u"image_dir_path_label")
        self.image_dir_path_label.setGeometry(QRect(70, 120, 78, 18))
        self.image_dir_path = QLineEdit(spider)
        self.image_dir_path.setObjectName(u"image_dir_path")
        self.image_dir_path.setGeometry(QRect(160, 120, 281, 21))
        self.ids = QLineEdit(spider)
        self.ids.setObjectName(u"ids")
        self.ids.setGeometry(QRect(160, 70, 281, 21))
        self.image_dir_path_select = QPushButton(spider)
        self.image_dir_path_select.setObjectName(u"image_dir_path_select")
        self.image_dir_path_select.setGeometry(QRect(460, 121, 113, 41))
        self.dir_path_select = QPushButton(spider)
        self.dir_path_select.setObjectName(u"dir_path_select")
        self.dir_path_select.setGeometry(QRect(460, 30, 113, 41))
        self.label = QLabel(spider)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(229, 10, 71, 20))
        self.logs_output = QTextEdit(spider)
        self.logs_output.setObjectName(u"logs_output")
        self.logs_output.setGeometry(QRect(10, 200, 561, 271))
        self.category = QRadioButton(spider)
        self.category.setObjectName(u"category")
        self.category.setGeometry(QRect(20, 70, 71, 20))
        self.product = QRadioButton(spider)
        self.product.setObjectName(u"product")
        self.product.setGeometry(QRect(90, 70, 61, 20))

        self.retranslateUi(spider)

        QMetaObject.connectSlotsByName(spider)
    # setupUi

    def retranslateUi(self, spider):
        spider.setWindowTitle(QCoreApplication.translate("spider", u"spider", None))
        self.crawl_btn.setText(QCoreApplication.translate("spider", u"\u5f00\u59cb\u722c\u53d6", None))
        self.logs_label.setText(QCoreApplication.translate("spider", u"\u8f93\u51fa\u65e5\u5fd7", None))
        self.dir_path.setText("")
        self.dir_path_label.setText(QCoreApplication.translate("spider", u"\u6587\u4ef6\u5b58\u50a8\u8def\u5f84", None))
        self.label_5.setText(QCoreApplication.translate("spider", u"\uff08\u53ef\u8f93\u5165\u591a\u4e2aid\uff0c\u7528\u82f1\u6587\u9017\u53f7\u9694\u5f00\uff09", None))
        self.download_image_btn.setText(QCoreApplication.translate("spider", u"\u5f00\u59cb\u4e0b\u8f7d\u56fe\u7247", None))
        self.image_dir_path_label.setText(QCoreApplication.translate("spider", u"\u56fe\u7247\u5b58\u50a8\u8def\u5f84", None))
        self.image_dir_path.setText("")
        self.ids.setText("")
        self.image_dir_path_select.setText(QCoreApplication.translate("spider", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.dir_path_select.setText(QCoreApplication.translate("spider", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.label.setText(QCoreApplication.translate("spider", u"kuajingyifan", None))
        self.category.setText(QCoreApplication.translate("spider", u"\u5206\u7c7bid", None))
        self.product.setText(QCoreApplication.translate("spider", u"\u4ea7\u54c1id", None))
    # retranslateUi

