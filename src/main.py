from crawler.spiders.tgdd.SPIDER import TgddSpider

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
    if os.path.isfile('text/items.jsonl'):
        os.remove('text/items.jsonl')
    if os.path.isfile('1_TGDD.log'):
        os.remove('1_TGDD.log')
    delete_data()
    process = CrawlerProcess(get_project_settings()) 
    process.crawl(TgddSpider)
    # d = process.join()
    # d.addCallback(lambda _: foo(process))

    process.start()
