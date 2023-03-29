from crawler.spiders.tgdd.computer_spider import ComputerSpider as TGDDComputerSpider
from crawler.spiders.tgdd.tablet_spider import TabletSpider as TGDDTabletSpider
from crawler.spiders.tgdd.printer_spider import PrinterSpider as TGDDPrinterSpider
from crawler.spiders.tgdd.watch_spider import WatchSpider as TGDDWatchSpider
from crawler.spiders.tgdd.screen_spider import ScreenSpider as TGDDScreenSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

if __name__ == '__main__':
    os.remove('text/items.jsonl')
    process = CrawlerProcess(get_project_settings())
    process.crawl(TGDDComputerSpider)
    process.crawl(TGDDTabletSpider)
    process.crawl(TGDDPrinterSpider)
    process.crawl(TGDDScreenSpider)
    process.crawl(TGDDWatchSpider)
    process.start()