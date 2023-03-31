from . import tgdd_spider
import scrapy
import re
from .tgdd_utils import *

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
        cpu = ', '.join(response.xpath(parameter_xpath("CPU")).getall())
        ram = normalize_disk_amount(response.xpath(parameter_xpath("RAM")).get())
        disk = ', '.join(filter(None, map(extract_disk, response.xpath(parameter_xpath("Ổ cứng")).getall())))
        screen = ', '.join(response.xpath(parameter_xpath("Màn hình")).getall())
        product_OS = ', '.join(response.xpath(parameter_xpath("Hệ điều hành")).getall())
        url = response.request.url

        # yield result of the current product
        # yield {
        #     "name": name,
        #     "price": price,
        #     "cpu": cpu,
        #     "ram": ram,
        #     "disk": disk,
        #     "screen": screen,
        #     "OS": product_OS,
        #     "url": url
        # }
        # add data to database
        sql = """
            INSERT INTO computer (name, price, cpu, ram, disk, screen, OS, url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id=id
        """
        crawl_cursor.execute(sql, (name, price, cpu, ram, disk, screen, product_OS, url))
        crawl_db.commit()
        # follow the link to other products
        yield from self.product_follow(response)
        