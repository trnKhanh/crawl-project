from . import tgdd_spider
import scrapy
import re
from . import tgdd_utils

class WatchSpider(tgdd_spider.TgddSpider):
    name = "tgdd_watch"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=7077&o=17&priceminmax=0-1000000&pi=0',
    ]

    def product_parse(self, response):
        # product name
        name = response.xpath("//h1/text()").get()
        # product price
        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        # normalize product price to integer
        if price: 
            price = re.sub(r"\D", "", price)
        # parse product parameter
        screen = ', '.join(response.xpath(tgdd_utils.parameter_xpath("Màn hình")).getall())
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "screen": screen,
            "url": url
        }

        # follow the link to other products
        yield from self.product_follow(response)
        