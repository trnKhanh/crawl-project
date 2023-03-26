import scrapy
import re
from scrapy.http import HtmlResponse
import json
from urllib.parse import urlencode

class TgddSpider(scrapy.Spider):
    name = 'tgdd'
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=522&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=42&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=7077&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5693&priceminmax=0-1000000&o=13&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=1262&o=7&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5697&o=7&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5698&o=7&priceminmax=0-1000000&pi=0',
    ]
    post_urls = [
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&priceminmax=0-1000000&pi=0',
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=522&o=17&priceminmax=0-1000000&pi=0',
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=42&priceminmax=0-1000000&o=17&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=7077&o=17&priceminmax=0-1000000&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=5693&priceminmax=0-1000000&o=13&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=1262&o=7&priceminmax=0-1000000&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=5697&o=7&priceminmax=0-1000000&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=5698&o=7&priceminmax=0-1000000&pi=0', 
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
    ]
    processed_url = urls
    def start_requests(self):
        for url in self.post_urls:
            yield scrapy.Request(   
                url=url["url"],
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }, 
                body=urlencode(url["data"]), 
                callback=self.parse,
            )

    def parse(self, response):
        self.processed_url.append(response.request.url)

        data = json.loads(response.text)
        products = HtmlResponse(url="https://www.thegioididong.com", body=data["listproducts"], encoding="utf-8")

        for product_link in products.xpath("//li/a[1]/@href").getall():
            url = response.urljoin(product_link)
            product_category = url.split('/')[-2]

            if url not in self.processed_url:
                if product_category == 'laptop':
                    yield scrapy.Request(url=url, callback=self.laptop_parse)
                elif product_category == 'may-tinh-bang':
                    yield scrapy.Request(url=url, callback=self.tablet_parse)
                elif product_category == 'dtdd':
                    yield scrapy.Request(url=url, callback=self.tablet_parse)
                elif product_category == 'dong-ho-thong-minh':
                    yield scrapy.Request(url=url, callback=self.watch_parse)
                elif product_category == 'may-in':
                    yield scrapy.Request(url=url, callback=self.printer_parse)
                elif product_category == 'muc-in':
                    yield scrapy.Request(url=url, callback=self.ink_parse)
                elif product_category == 'man-hinh-may-tinh':
                    yield scrapy.Request(url=url, callback=self.screen_parse)
                elif product_category == 'may-tinh-de-ban':
                    yield scrapy.Request(url=url, callback=self.pc_parse)

        for pi in range(20, data["total"], 20):
            url=response.request.url.replace("pi=0", f"pi={int(pi/20)}")
            if url not in self.processed_url:
                yield scrapy.Request(   
                    url=url,
                    method=response.request.method,
                    headers=response.request.headers,
                    body=response.request.body, 
                    callback=self.parse,
                )

    def laptop_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        cpu = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'CPU')]]/following-sibling::*[1]/*/text()").getall())
        
        ram = response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'RAM')]]/following-sibling::*[1]/*/text()").get()
        
        disk = ', '.join(filter(None, map(extract_disk, response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Ổ cứng')]]/following-sibling::*[1]/*/text()").getall())))
        
        screen = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Màn hình')]]/following-sibling::*[1]/*/text()").getall())
        
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
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.laptop_parse)

    def tablet_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()
        if name == None:
            name = response.request.url.split('/')[-1].replace('-', ' ')

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        chip = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Chip')]]/following-sibling::*[1]/*/text()").getall())
        
        ram = response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'RAM')]]/following-sibling::*[1]/*/text()").get()
        
        disk = ', '.join(filter(None, map(extract_disk, response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Dung lượng lưu trữ')]]/following-sibling::*[1]/*/text()").getall())))
        
        screen = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Màn hình')]]/following-sibling::*[1]/*/text()").getall())
        
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "chip": chip,
            "ram": ram,
            "disk": disk,
            "screen": screen,
            "url": url
        }

        # follow the link to other products
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.tablet_parse)

    def watch_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()
        if name == None:
            name = response.request.url.split('/')[-1].replace('-', ' ')

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)
        
        screen = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Màn hình')]]/following-sibling::*[1]/*/text()").getall())
        
        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "screen": screen,
            "url": url
        }

        # follow the link to other products
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.watch_parse)

    def printer_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        printer_type = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Loại máy')]]/following-sibling::*[1]/*/text()").getall())
        
        print_speed = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Tốc độ in')]]/following-sibling::*[1]/*/text()").getall())
        
        ink_type = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Loại mực in')]]/following-sibling::*[1]/*/text()").getall())

        print_quality = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Chất lượng in')]]/following-sibling::*[1]/*/text()").getall())

        paper_type = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Giấy in')]]/following-sibling::*[1]/*/text()").getall())

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
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.printer_parse)

    def ink_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        url = response.request.url

        # yield result of the current product
        yield {
            "name": name,
            "price": price,
            "url": url
        }

        # follow the link to other products
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.ink_parse)

    def screen_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        screen_type = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Loại màn hình')]]/following-sibling::*[1]/*/text()").getall())
        
        screen_size = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Màn hình')]]/following-sibling::*[1]/*/text()").getall())
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
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.screen_parse)

    def pc_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()

        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)

        cpu = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'CPU')]]/following-sibling::*[1]/*/text()").getall())
        
        ram = response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'RAM')]]/following-sibling::*[1]/*/text()").get()
        
        disk = ', '.join(filter(None, map(extract_disk, response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Ổ cứng')]]/following-sibling::*[1]/*/text()").getall())))
        
        screen = ', '.join(response.xpath("//*[contains(@class, 'parameter')]/descendant::li/*[descendant-or-self::*[contains(text(), 'Màn hình')]]/following-sibling::*[1]/*/text()").getall())
        
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
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.pc_parse)
        
def extract_disk(disk):
    pattern = r'(\d+\s*\w*?B\s*(SSD|HDD|EMMC))|((SSD|HDD|EMMC)\s*\d+\s*\w*?B)'
    found = re.search(pattern, disk.upper())
    if found:
        return found.group()
    else:
        pattern = r'\d+\s*\w*?B'
        found = re.search(pattern, disk.upper())
        if found:
            return found.group()