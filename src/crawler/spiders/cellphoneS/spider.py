import scrapy
import json
from .data import *
from .utils import *
from crawler.items import ProductItem

class GearvnHomeSpider(scrapy.Spider):
    name = 'CellPhoneS_spider'
    urls = ['https://cellphones.com.vn/']

    category_urls = [
        'https://cellphones.com.vn/mobile.html',
        'https://cellphones.com.vn/laptop.html',
        'https://cellphones.com.vn/tablet.html',
        'https://cellphones.com.vn/do-choi-cong-nghe.html',
        'https://cellphones.com.vn/may-tinh-de-ban.html',
    ]
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # for url in self.category_urls:
        #     yield scrapy.Request(url=url, callback=self.parse_category)
            
    def parse(self, response):
        for link in response.xpath('descendant::div[contain(@class, "menu-tree")]/child::*[1]/@href').get():
            url = response.urljoin(link)
            print(url)
            # if url[-4:] == '-ldp':
            #     url = url[:-4]
            # if 'https://cellphones.com.vn/' in url:
            #     yield scrapy.Request(url=url, callback=self.parse_category)

    
    def parse_category(self, response):
        pass
        
    def parse_product(self, response):
        pass
    
    