from . import tgdd_spider
import scrapy
import re
from . import tgdd_utils

class ComputerSpider(tgdd_spider.TgddSpider):
    name = "tgdd_computer"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5698&o=7&priceminmax=0-1000000&pi=0',
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
        cpu = ', '.join(response.xpath(tgdd_utils.parameter_xpath("CPU")).getall())
        ram = tgdd_utils.normalize_disk_amount(response.xpath(tgdd_utils.parameter_xpath("RAM")).get())
        disk = ', '.join(filter(None, map(tgdd_utils.extract_disk, response.xpath(tgdd_utils.parameter_xpath("Ổ cứng")).getall())))
        screen = ', '.join(response.xpath(tgdd_utils.parameter_xpath("Màn hình")).getall())
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "screen": screen,
            "url": url
        }

        # follow the link to other products
        yield from self.product_follow(response)
        