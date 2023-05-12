import scrapy
import json
from .data import *
from .utils import *
from crawler.items import ProductItem

class GearvnSpider(scrapy.Spider):
    name = 'GearvnHome_spider'
    start_urls = ['https://gearvn.com']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(   
                url=url,
                callback=self.parse,
            )
            
    
    def parse(self, response):
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

        for product in response.css('.product-row'):
            product_link = product.css('a::attr(href)').get()
            product_link = response.urljoin(product_link)
            
            thumb_nail_product = product.xpath('descendant::img[contains(@class, "thumbnail")]/@src').get()
            thumb_nail_product = response.urljoin(thumb_nail_product)
            
            yield scrapy.Request(
                url=response.urljoin(product_link),
                callback=self.parse_product,
                meta=dict(product_url = product_link,
                          thumbnail_image=thumb_nail_product,
                )
            )
        
    def parse_product(self, response):
        product_frame = response.css('.container')
        if not product_frame:
            return

        # get image
        image_urls = [response.meta.get("thumbnail_image")]
        product_urls = response.meta.get("product_url")
        #price = [response.meta.get("product_price")]
        price = response.xpath('descendant::span[contains(@class, "product_sale_price")]/text()').get()[:-3]
        product_name = (response.css('.page_content').css('h1::text').get()[8:])[:-8]
        category_table = get_category_table(product_name)
        dict={
            "name" : product_name,
            "price" : price_to_int(price),
            "url" : product_urls,
        }
            
        for product_parameter, product_parameter_alias in category_parameter[category_table].items():
            #print(product_parameter)
            dict[product_parameter] = None
            for alias in product_parameter_alias:
                Myxpath = parameter_xpath(alias)
                dict[product_parameter] = response.xpath(Myxpath).get()
                if dict[product_parameter] != None:
                    break

        yield ProductItem(category=category_table,
                          image_paths=image_urls,
                          product_info=dict,
                          website="Gearvn")
    
    