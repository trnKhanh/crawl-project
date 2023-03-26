import scrapy
import re
from scrapy.http import HtmlResponse
import json
import requests
from urllib.parse import urlencode

class TgddSpider(scrapy.Spider):
    name = 'tgdd'
    urls = [
        # 'https://www.thegioididong.com/laptop#c=44&o=17&pi=2',
        'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&pi=0'
    ]
    post_urls = [
        {
            "url": 'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&pi=0',
            "data": {"IsParentCate": False, "IsShowCompare": True, "prevent": True}
        },
    ]
    processed_url = []
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
        products = HtmlResponse(url="https://www.thegioididong.com/laptop", body=data["listproducts"], encoding="utf-8")

        for product_link in products.xpath("//li/a[1]/@href").getall():
            url = response.urljoin(product_link)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.product_parse)

        if response.request.url in self.urls:
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
    def product_parse(self, response):
        self.processed_url.append(response.request.url)

        name = response.xpath("//h1/text()").get()
        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        if price: 
            price = re.sub("\D", "", price)
        cpu = ', '.join(response.xpath("//li/p[contains(text(), 'CPU')]/following-sibling::*[1]/*/text()").getall())
        ram = response.xpath("//li/p[contains(text(), 'RAM')]/following-sibling::*[1]/*/text()").get()
        disk = ', '.join(filter(None, map(extract_disk, response.xpath("//li/p[contains(text(), 'Ổ cứng')]/following-sibling::*[1]/*/text()").getall())))
        screen = ', '.join(response.xpath("//li/p[contains(text(), 'Màn hình')]/following-sibling::*[1]/*/text()").getall())
        url = response.request.url
        yield {
            "name": name,
            "price": price,
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "screen": screen,
            "url": url
        }

        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            if url not in self.processed_url:
                yield scrapy.Request(url=url, callback=self.product_parse)

        
def extract_disk(disk):
    found = re.search(r'\d+\s*\w*?B\s*(SSD|HDD|EMMC)', disk.upper())
    if found:
        found = found.group()
        return found