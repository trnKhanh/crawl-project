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
    post_data = urlencode({"IsParentCate": False, "IsShowCompare": True, "prevent": True})

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(   
                url=url,
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }, 
                body=self.post_data, 
                callback=self.parse,
            )

    def parse(self, response):
        data = json.loads(response.text)
        products = HtmlResponse(url="https://www.thegioididong.com", body=data["listproducts"], encoding="utf-8")
        
        # find and follow to product pages
        for product_link in products.xpath("//li/a[1]/@href").getall():
            url = response.urljoin(product_link)
            yield scrapy.Request(url=url, callback=self.product_parse)

        # request more data from tgdd's database
        for pi in range(20, data["total"], 20):
            url=response.request.url.replace("pi=0", f"pi={int(pi/20)}")
            
            yield scrapy.Request(   
                url=url,
                method=response.request.method,
                headers=response.request.headers,
                body=response.request.body, 
                callback=self.parse,
            )
    def product_parse(self, response):
        pass
    
    def product_follow(self, response):
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.product_parse)
        
