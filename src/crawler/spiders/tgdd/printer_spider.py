from . import tgdd_spider
import scrapy
import re
from . import tgdd_utils

class PrinterSpider(tgdd_spider.TgddSpider):
    name = "tgdd_printer"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=5693&priceminmax=0-1000000&o=13&pi=0',
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
        printer_type = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Loại máy')).getall())
        print_speed = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Tốc độ in')).getall())
        ink_type = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Loại mực in')).getall())
        print_quality = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Chất lượng in')).getall())
        paper_type = ', '.join(response.xpath(tgdd_utils.parameter_xpath('Giấy in')).getall())

        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "printer_type": printer_type,
            "print_speed": print_speed,
            "ink_type": ink_type,
            "print_quality": print_quality,
            "paper_type": paper_type,
            "url": url
        }

        # follow the link to other products
        yield from self.product_follow(response)
        