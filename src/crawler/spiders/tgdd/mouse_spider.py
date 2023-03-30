from . import tgdd_spider
import re
from . import tgdd_utils

class MouseSpider(tgdd_spider.TgddSpider):
    name = "tgdd_mouse"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=86&o=14&priceminmax=0-1000000&pi=0',
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
        dpi = ', '.join(response.xpath(tgdd_utils.parameter_xpath("Độ phân giải")).getall())
        connect_type = ', '.join(response.xpath(tgdd_utils.parameter_xpath("Cách kết nối")).getall())
        brand = ', '.join(response.xpath(tgdd_utils.parameter_xpath("Hãng")).getall())
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "dpi": dpi,
            "connect_type": connect_type,
            "brand": brand,
            "url": url
        }

        # follow the link to other products
        yield from self.product_follow(response)
        