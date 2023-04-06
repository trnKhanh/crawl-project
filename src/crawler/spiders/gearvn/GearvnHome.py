import scrapy
import re
import json
from .Classfication import *

class GearvnHomeSpider(scrapy.Spider):
    name = 'GearvnHome_spider'
    start_urls = ['https://gearvn.com']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(   
                url=url,
                callback=self.parse,
            )
    
    def parse(self, response):
        #data = json.loads(response.text)
        for category in response.css('.sub-cat-item-filter'):
            category_link = category.css('::attr(href)').get()
            yield scrapy.Request(
                url = response.urljoin(category_link),
                callback= self.parse_category,
            )
    
    def parse_category(self, response):
        # Check collection page
        category_frame = response.css('.container')
        
        if not category_frame:
            return
        # print(1)
        for product in response.css('.product-row'):
            product_link = product.css('a::attr(href)').get()
            yield scrapy.Request(
                url=response.urljoin(product_link),
                callback=self.parse_product,
            )
        
    def parse_product(self, response):
        product_frame = response.css('.container')
        if not product_frame:
            return
        for info in response.css('.page_content'):
            product_name = (info.css('h1::text').get()[8:])[:-8]
            type = parse(product_name)
            details = parse_following_type(type, response)
            print(details)
        pass
    