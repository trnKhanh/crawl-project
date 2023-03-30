from . import tgdd_spider
import re
from . import tgdd_utils
import scrapy

class AllSpider(tgdd_spider.TgddSpider):
    name = "tgdd_all"
    urls = [
        # "https://www.thegioididong.com/dong-ho-deo-tay/certina-c035-410-36-087-00-nam?src=osp&itm_source=detail&itm_medium=product_card&itm_campaign=viewedhttps://www.thegioididong.com/dong-ho-deo-tay/certina-c035-410-36-087-00-nam?src=osp&itm_source=detail&itm_medium=product_card&itm_campaign=viewed",
        'https://www.thegioididong.com',
    ]
    forbidden = [
        "tien-ich",
        "game-app",
        "tin-tuc",
        "hoi-dap",
    ]
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        # product name
        name = response.xpath("//h1/text()").get()
        # product price
        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        # normalize product price to integer
        if price: 
            price = re.sub(r"\D", "", price)
        # parse product parameter
        url = response.request.url
        # yield result of the current product
        if name and price:
            yield {
                "name": name,
                "price": price,
                "url": url
            }

        # follow the link to other products
        for link in response.xpath("//a/@href").getall():
            url = response.urljoin(link)
            url = url.split("?")[0].split("#")[0]
            length = len(url.split('/'))
            if length > 3:
                section = url.split('/')[3]
            else:
                section = None
            if "https://www.thegioididong.com" in url and (length == 4 or length == 5) and section not in self.forbidden:
                yield scrapy.Request(url=url, callback=self.parse)
        