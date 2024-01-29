# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
import urllib.request
import os

from scrapy.utils.project import get_project_settings


# from KJYF_spider.main import get_data


class KjyfSpiderPipeline:
    settings = get_project_settings()

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(self.settings.get('CUSTOM_EXECL_HEADERS'))

    def process_item(self, item, spider):
        # 兼容文件夹不存在的情况
        execl_path = item['dir_path'].rstrip("\\")
        if not os.path.exists(execl_path):
            os.makedirs(execl_path)
        line = [item['cate_id'], item['p_id'], item['title'], item['price'], item['spec'], item['description'],
                item['images']]
        self.ws.append(line)
        self.wb.save(execl_path + '/' + self.settings.get('CUSTOM_EXECL_FILE_NAME'))
        return item
