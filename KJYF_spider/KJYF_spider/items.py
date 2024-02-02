# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KjyfSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 分类id
    cate_id = scrapy.Field()
    # 产品id
    p_id = scrapy.Field()
    # 产品标题
    title = scrapy.Field()
    # 产品图片
    images = scrapy.Field()
    # 产品价格
    price = scrapy.Field()
    # 产品规格
    spec = scrapy.Field()
    # 文件存储路径
    dir_path = scrapy.Field()
