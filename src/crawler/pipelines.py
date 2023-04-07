# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import mysql.connector

class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
            
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item["image_paths"] = image_paths
        return item
        
class SQLPipeline:
    def open_spider(self, spider):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="crawl_database"
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.commit()
        
    def process_item(self, item, spider):
        column_names = (', '.join(item["product_info"].keys()) + ', image_path' + ', website')
        sql = f"""
            INSERT INTO {item["category"]} ({column_names}) 
            VALUES ({("%s," * (len(item["product_info"]) + 2)).strip(',')})
            ON DUPLICATE KEY UPDATE id=id
        """
        # print(sql)
        new_row = list(item["product_info"].values())

        if "image_paths" in item:
            for image_path in item["image_paths"]:
                new_row.append(image_path)
        else:
            new_row.append(None)
        
        new_row.append(item["website"])
        # print(sql)
        # print(new_row)
        self.cursor.execute(sql, new_row)
        return item