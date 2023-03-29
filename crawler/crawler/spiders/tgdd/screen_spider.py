from . import tgdd_spider
import scrapy
import re
from . import tgdd_utils

class ScreenSpider(tgdd_spider.TgddSpider):
    name = "tgdd_screen"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=5697&o=7&priceminmax=0-1000000&pi=0',
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
        screen_type = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Loại màn hình')).getall())
        screen_size = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Màn hình')).getall())
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "screen_type": screen_type,
            "screen_size": screen_size,
            "url": url
        }

        # follow the link to other products
        yield from self.product_follow(response)
        