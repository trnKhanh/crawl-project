import scrapy
import json
from .data import *
from .utils import *
from crawler.items import ProductItem
from scrapy_playwright.page import PageMethod

class CellphoneSSpider(scrapy.Spider):
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
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                meta=dict())
        # for url in self.category_urls:
        #     yield scrapy.Request(url=url, callback=self.parse_category)
            
    def parse(self, response):
        for link in response.xpath('descendant::div[contains(@class, "menu-tree")]/*/@href').getall():
            url = response.urljoin(link)
            print(url)
            # if 'https://cellphones.com.vn/' in url:
            yield scrapy.Request(
                url=url, 
                callback=self.parse_category,
                meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.l-pd", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "div.st-slider img", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a", timeout=10 * 1000, state='attached'),
                    PageMethod("click", ".st-pd-table-viewDetail > a")
                ],
                name=None,
            ))
            return

    def parse_category(self, response):
        category_box = response.xpath('//div[contains(@class, "item-categories-outer")]/child::*[1]').getall()
        print(category_box)
        return
        for category in category_box:
            url = response.urljoin(category.xpath('/@href').get())
            print(url)
            #yield scrapy.Request(url=url, callback=self.parse_sub_category)        
        return
    
    def parse_sub_category(self, response):
        product_box = response.xpath('//div[contains(@class, "product-info")]')
        for product in product_box:
            product_name = product.xpath('descendant::div[contains(@class, "product__name")]/*/text()').get()
            product_url = product.xpath('child::[1]/@href').get()
            image_url = product.xpath('descendant::img[1]/@src').get()
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta=dict(
                    product_name=product_name,
                    product_url=product_url,
                    image_url=image_url,
                )
            )
        pass
    
    def parse_product(self, response):
        product_name = response.meta.get("product_name")
        product_link = response.meta.get("product_url")
        image_url = response.meta.get("image_url")
        yield {
            'name':product_name,
            'link':product_link,
            'image':image_url,
        }
    
    