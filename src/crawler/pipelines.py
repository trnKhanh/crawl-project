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
from .parse_utils import *

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

    # def close_spider(self, spider):
    #     pass
        
    def process_item(self, item, spider):
        if "cpu" in item['product_info']:
            item['product_info']['cpu'] = extract_cpu(item['product_info']['cpu'])
        if "ram" in item['product_info']:
            item['product_info']['ram'] = extract_byte(item['product_info']['ram'])
        if "screen" in item['product_info']:
            item['product_info']['screen'] = extract_screen(item['product_info']['screen'])
        if 'screen_size' in item['product_info']:
            item['product_info']['screen_size'] = extract_screen(item['product_info']['screen_size'])
        if 'disk' in item['product_info']:
            item['product_info']['disk'] = extract_disk(item['product_info']['disk'])

        column_names = (', '.join(item["product_info"].keys()) + ', image_path' + ', website')
        sql = f"""
            INSERT INTO {item["category"]} ({column_names}) 
            VALUES ({("%s," * (len(item["product_info"]) + 2)).strip(',')})
            ON DUPLICATE KEY UPDATE id=id
        """
        # print(sql)
        new_row = list(item["product_info"].values())

        if "image_paths" in item:
            for image_path in item["image_urls"]:
                new_row.append(image_path)
        else:
            new_row.append(None)
        
        new_row.append(item["website"])

        # print(sql)
        # print(new_row)
        self.cursor.execute(sql, new_row)
        self.db.commit()
        return item

