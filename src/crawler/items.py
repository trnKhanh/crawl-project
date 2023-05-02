# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class ProductItem(scrapy.Item):
    category = scrapy.Field() # table_name in sql
    image_urls = scrapy.Field() # array
    product_info = scrapy.Field() # parameter(include name, price, url, and other parameters (e.g cpu, ram,...))
    image_paths = scrapy.Field() # do not care about
    website = scrapy.Field() # set this to the web you crawl

# image_urls = [response.urljoin(link)]
