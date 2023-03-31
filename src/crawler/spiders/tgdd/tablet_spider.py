from . import tgdd_spider
import re
from .tgdd_utils import *

class TabletSpider(tgdd_spider.TgddSpider):
    name = "tgdd_tablet"
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=522&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=42&o=17&priceminmax=0-1000000&pi=0',
    ]
    
    def product_parse(self, response):
        # product name
        name = response.xpath("//h1/text()").get()
        if name:
            # product price
            price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
            # normalize product price to integer
            if price: 
                price = re.sub(r"\D", "", price)
            # parse product parameter
            chip = ', '.join(response.xpath(parameter_xpath("Chip")).getall())
            ram = normalize_disk_amount(response.xpath(parameter_xpath("RAM")).get())
            disk = ', '.join(filter(None, map(extract_disk, response.xpath(parameter_xpath("Dung lượng lưu trữ")).getall())))
            screen = ', '.join(response.xpath(parameter_xpath("Màn hình")).getall())
            product_OS = ', '.join(response.xpath(parameter_xpath("Hệ điều hành")).getall())
            url = response.request.url

            # yield result of the current product
            # yield {
            #     "name": name,
            #     "price": price,
            #     "chip": chip,
            #     "ram": ram,
            #     "disk": disk,
            #     "screen": screen,
            #     "OS": product_OS,
            #     "url": url
            # }
            # add data to database
            sql = """
                INSERT INTO tablet (name, price, chip, ram, disk, screen, OS, url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE id=id
            """
            crawl_cursor.execute(sql, (name, price, chip, ram, disk, screen, product_OS, url))
            crawl_db.commit()
        else:
            self.preorder_parse(response)

        # follow the link to other products
        yield from self.product_follow(response)

    def preorder_parse(self, response):
        for section in response.xpath('//section[contains(@class, "config")]'):
            id = '#' + section.xpath('self::*/@id').get()
            #product name
            name = section.xpath(f'descendant::*[contains(@href, "{id}")]/text()').get()
            if name == None:
                name = response.request.url.split('/')[-1].replace('-', ' ')
            # product price
            price = section.xpath('descendant::*[contains(text(), "Giá")]/*/text()').get()
            # normalize product price to integer
            if price: 
                price = re.sub(r"\D", "", price)
            # product parameter
            chip = ', '.join(section.xpath(parameter_xpath("Chip")).getall())
            ram = normalize_disk_amount(section.xpath(parameter_xpath("RAM")).get())
            disk = ', '.join(filter(None, map(extract_disk, section.xpath(parameter_xpath("Dung lượng lưu trữ")).getall())))
            screen = ', '.join(section.xpath(parameter_xpath("Màn hình")).getall())
            product_OS = ', '.join(response.xpath(parameter_xpath("Hệ điều hành")).getall())
            url = response.request.url

            # yield result of the current product
            # yield {
            #     "name": name,
            #     "price": price,
            #     "chip": chip,
            #     "ram": ram,
            #     "disk": disk,
            #     "screen": screen,
            #     "url": url
            # }
            # add data to database
            sql = """
                INSERT INTO tablet (name, price, chip, ram, disk, screen, OS, url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE id=id
            """
            crawl_cursor.execute(sql, (name, price, chip, ram, disk, screen, product_OS, url))
            crawl_db.commit()
            
            
        