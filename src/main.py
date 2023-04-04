import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler.spiders.gearvn.GearvnHome import GearvnHomeSpider

def crawling():
    print("Crawling...")
    process = CrawlerProcess(get_project_settings())
    process.crawl(GearvnHomeSpider)
    process.start()
    print("End processing")
    pass
    
if __name__ == '__main__':
    if(os.path.isfile('items.jsonl')) :
        os.remove('items.jsonl')
    if(os.path.isfile('gearvn.log')):
        os.remove('gearvn.log')
    crawling()