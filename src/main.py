from crawler.spiders.tgdd.computer_spider import ComputerSpider as TGDDComputerSpider
from crawler.spiders.tgdd.tablet_spider import TabletSpider as TGDDTabletSpider
from crawler.spiders.tgdd.printer_spider import PrinterSpider as TGDDPrinterSpider
from crawler.spiders.tgdd.watch_spider import WatchSpider as TGDDWatchSpider
from crawler.spiders.tgdd.screen_spider import ScreenSpider as TGDDScreenSpider
from crawler.spiders.tgdd.mouse_spider import MouseSpider as TGDDMouseSpider
from crawler.spiders.tgdd.keyboard_spider import KeyboardSpider as TGDDKeyboardSpider
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
    process.crawl(TGDDComputerSpider)
    process.crawl(TGDDTabletSpider)
    process.crawl(TGDDPrinterSpider)
    process.crawl(TGDDScreenSpider)
    process.crawl(TGDDWatchSpider)
    process.crawl(TGDDMouseSpider)
    process.crawl(TGDDKeyboardSpider)
    d = process.join()
    d.addCallback(lambda _: foo(process))

    process.start()
