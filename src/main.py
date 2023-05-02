
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.cellphoneS.spider import CellphoneSSpider
from crawler.spiders.gearvn.spider import GearvnSpider
from crawler.spiders.tgdd.SPIDER import TgddSpider
from crawler.spiders.fpt.SPIDER import FPTSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="crawl_database"
)
cursor = db.cursor()
def delete_data():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]}")
    db.commit()

if __name__ == '__main__':
    if os.path.isfile('CRAWLER_SPIDER.log'):
        os.remove('CRAWLER_SPIDER.log')
    delete_data()
    process = CrawlerProcess(get_project_settings()) 
    process.crawl(TgddSpider).addCallback(lambda _: process.crawl(FPTSpider))\
    process.crawl(GearvnSpider)
    process.crawl(CellphoneSSpider)
    # d = process.join()
    # d.addCallback(lambda _: foo(process))

    process.start()
