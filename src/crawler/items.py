# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class ProductItem(scrapy.Item):
    category = scrapy.Field() # table_name in sql
    product_info = scrapy.Field() # parameter of product (include name, price, url, and other parameters (e.g cpu, ram,...))
    image_paths = scrapy.Field() # path to thumbnail image of product
    website = scrapy.Field() # name of the web you crawl

# image_urls = [response.urljoin(link)]
