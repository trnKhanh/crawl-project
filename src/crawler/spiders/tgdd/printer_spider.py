from . import tgdd_spider
import re
from .tgdd_utils import *

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
        printer_type = ', '.join(response.xpath(parameter_xpath('Loại máy')).getall())
        print_speed = ', '.join(response.xpath(parameter_xpath('Tốc độ in')).getall())
        ink_type = ', '.join(response.xpath(parameter_xpath('Loại mực in')).getall())
        print_quality = ', '.join(response.xpath(parameter_xpath('Chất lượng in')).getall())
        paper_type = ', '.join(response.xpath(parameter_xpath('Giấy in')).getall())
        brand = ', '.join(response.xpath(parameter_xpath("Hãng")).getall())
        url = response.request.url

        # yield result of the current product
        # yield {
        #     "name": name,
        #     "price": price,
        #     "printer_type": printer_type,
        #     "print_speed": print_speed,
        #     "ink_type": ink_type,
        #     "print_quality": print_quality,
        #     "paper_type": paper_type,
        #     "brand": brand,
        #     "url": url
        # }
        # add data to database
        sql = """
            INSERT INTO printer (name, price, printer_type, print_speed, ink_type, print_quality, paper_type, brand, url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id=id
        """
        crawl_cursor.execute(sql, (name, price, printer_type, print_speed, ink_type, print_quality, paper_type, brand, url))
        crawl_db.commit()
        # follow the link to other products
        yield from self.product_follow(response)
        