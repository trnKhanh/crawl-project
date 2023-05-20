
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.cellphoneS.spider import CellphoneSSpider
from crawler.spiders.gearvn.spider import GearvnSpider
from crawler.spiders.tgdd.spider import TgddSpider
from crawler.spiders.fpt.spider import FPTSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import mysql.connector
import time

import schedule

from multiprocessing import Process

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

def crawl():
    delete_data()
    process = CrawlerProcess(get_project_settings()) 
    process.crawl(TgddSpider).addCallback(
        lambda _: process.crawl(FPTSpider).addCallback(
            lambda _: process.crawl(GearvnSpider).addCallback(
                lambda _: process.crawl(CellphoneSSpider)
        )))

    process.start()

def start_crawl():
    p = Process(target=crawl)
    p.start()
    p.join()

if __name__ == '__main__':
    # schedule.every().day.at("00:00").do(start_crawl)
    schedule.every(3).hours.do(start_crawl)
    start_crawl()
    while True:
        schedule.run_pending()

        time.sleep(1)
