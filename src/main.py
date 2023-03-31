import scrapy

class MydomainSpider(scrapy.Spider):
    name = "mydomain"
    allowed_domains = ["gearvn.com"]
    start_urls = ["http://gearvn.com/"]

    def parse(self, response):
        pass
