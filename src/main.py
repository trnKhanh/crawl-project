from crawler.spiders.tgdd.tgdd_spider import TgddSpider
from crawler.spiders.tgdd.all_spider import AllSpider as TGDDAllSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

def foo(process):
    print("Crawl the rest...")
    process.crawl(TGDDAllSpider)

if __name__ == '__main__':
    if os.path.isfile('text/items.jsonl'):
        os.remove('text/items.jsonl')
    if os.path.isfile('tgdd.log'):
        os.remove('tgdd.log')
    process = CrawlerProcess(get_project_settings()) 
    process.crawl(TgddSpider)
    # d = process.join()
    # d.addCallback(lambda _: foo(process))

    process.start()
