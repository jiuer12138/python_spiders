import time

import scrapy
from scrapy import signals
from utils import format_str
from selenium import webdriver
from items import KjyfSpiderItem


class KjyfSpider(scrapy.Spider):
    name = "KJYF"
    allowed_domains = ["www.kuajingyifan.com"]
    start_urls = []
    base_url = 'https://www.kuajingyifan.com/zh-CN/'

    def __init__(self, *args, **kwargs):
        super(KjyfSpider, self).__init__(*args, **kwargs)
        # 初始化Selenium WebDriver 并且不打开chrome爬取
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.q = kwargs.get('q')
        self.ids = kwargs.get('ids')
        self.is_cate = kwargs.get('is_cate')
        self.dir_path = kwargs.get('dir_path')
        # 判断分类还是商品的ids并转换为数组拼接url
        ids_list = self.ids.rstrip(',').split(',')
        self.start_urls = self.stitching_url(ids_list, self.is_cate)

    # 信号可选类型  from scrapy import signals 中可以看到
    # engine_started = object()
    # engine_stopped = object()
    # spider_opened = object()
    # spider_idle = object()
    # spider_closed = object()
    # spider_error = object()
    # request_scheduled = object()
    # request_dropped = object()
    # response_received = object()
    # response_downloaded = object()
    # item_scraped = object()
    # item_dropped = object()
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KjyfSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_closed(self, spider):
        self.q.put(format_str("爬取结束"))

    def spider_opened(self, spider):
        self.q.put(format_str("爬取开始"))

    def stitching_url(self, ids, is_cate=True):
        if is_cate:
            return [(self.base_url + 'c/' + str(i)) for i in ids]
        else:
            return [(self.base_url + 'p/' + str(i) + '/a') for i in ids]

    def get_updated_response(self, url, sleep=0):
        # 使用Selenium控制浏览器打开初始URL
        self.driver.get(url)
        time.sleep(sleep)
        # 获取更新后的页面源代码
        updated_html = self.driver.page_source
        return scrapy.http.HtmlResponse(url=self.driver.current_url, body=updated_html,
                                        encoding='utf-8')

    # 处理根据分类id爬取商品id
    def handle_cate_href(self, url):
        updated_response = self.get_updated_response(url)
        urls = updated_response.xpath('//*[@id="category"]/div[2]/div[2]/div/div//div/a/@href').extract()
        return [url.replace('/zh-CN/p/', '').replace('/a', '') for url in urls if url.endswith('/a')]

    def parse(self, response, *args, **kwargs):
        self.q.put(format_str("开始爬取url:" + response.url))
        # updated_response = self.get_updated_response(response.url)
        if self.is_cate:
            pages = response.xpath('//*[@id="category"]/div[2]/div[2]/div/nav/a/@href').extract()
            max_page = pages[-1][pages[-1].rfind('=') + 1:]
            p_num = response.xpath('//*[@id="category"]/div[1]/div[2]/div[2]/span[2]/text()').get()
            self.q.put(format_str('当前分类共有' + p_num + '件商品，共' + max_page + '页'))
            p_ids = []
            for p in range(1, int(max_page) + 1):
                self.q.put(format_str('开始爬取第' + str(p) + '的页商品id'))
                p_ids.extend(self.handle_cate_href(response.url + '/?page=' + str(p)))
                self.q.put(format_str('结束爬取第' + str(p) + '的页商品id'))
            self.q.put(format_str('共' + str(len(p_ids)) + '件商品id爬取成功'))
            if '?page=' in response.url:
                current_c_id = response.url[response.url.rfind('/') + 1:response.url.rfind('?page=')]
            else:
                current_c_id = response.url[response.url.rfind('/') + 1:]
            for url in self.stitching_url(p_ids, False):
                item = self.parse_product(url, current_c_id)
                yield item
        else:
            item = self.parse_product(response.url)
            yield item

    # 解析商品详情页
    def parse_product(self, url, cate_id=-1):
        self.q.put(format_str('正在爬取链接：' + url))
        res = self.get_updated_response(url, 5)
        # 提取数据
        title = res.xpath('//*[@id="product"]/div/div[2]/div[1]//h1/text()').get()
        images = res.xpath('//*[@id="product"]/section[1]/div[2]//img/@src').getall()
        price = res.xpath('//*[@id="product"]/div/div[2]/div[2]//text()').getall()
        spec = res.xpath(
            '//*[@id="product"]/div/div[2]/div[3]/div/div/div[1]//text()').getall()
        spec = [x.strip() for x in spec if x.strip() != '']
        separator = ','
        item = KjyfSpiderItem()
        item['cate_id'] = cate_id
        if title is not None:
            item['title'] = title.strip()
        if images is not None:
            item['images'] = separator.join(images)
        if price is not None:
            price = [p for p in price if p.strip() != '']
            item['price'] = price[0].strip()
        if spec is not None:
            item['spec'] = separator.join(spec)
        item['p_id'] = url.split('/')[-2]
        item['dir_path'] = self.dir_path
        return item
