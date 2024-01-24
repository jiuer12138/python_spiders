import scrapy


class KjyfSpider(scrapy.Spider):
    name = "KJYF"
    allowed_domains = ["www.kuajingyifan.com"]
    start_urls = ["http://www.kuajingyifan.com/"]

    def parse(self, response, *args, **kwargs):
        pass
