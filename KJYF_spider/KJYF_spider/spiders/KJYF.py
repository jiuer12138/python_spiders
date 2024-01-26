import scrapy
from scrapy import signals
from utils import format_str
from selenium import webdriver


class KjyfSpider(scrapy.Spider):
    name = "KJYF"
    allowed_domains = ["www.kuajingyifan.com"]
    start_urls = ['https://www.kuajingyifan.com']
    base_url = 'https://www.kuajingyifan.com/'

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
        self.images_path=kwargs.get('images_path')
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

    def parse(self, response, *args, **kwargs):
        print("==========")
        print(self.is_cate)
        print("==========")
        print(self.ids)
        print("==========")
        print(self.dir_path)
        print("==========")
        print(self.images_path)
        print("==========")
        pass

    # def close(spider, reason):
    #     spider.q.put('爬取结束')
    #     print('爬取结束')
