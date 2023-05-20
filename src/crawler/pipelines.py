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

# class CustomImagePipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url)
            
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         item["image_paths"] = image_paths
#         return item
class CleansePipeline:
    def process_item(self, item, spider):
        for name, data in item['product_info'].items():
            if name.lower() != 'url':
                item['product_info'][name] = remove_extra(data)
        
        if "name" in item['product_info']:
            item['product_info']['name'] = extract_name(item['product_info']['name'])

        if "price" in item['product_info']:
            item['product_info']['price'] = extract_price(item['product_info']['price'])

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
        
        if 'brand' in item['product_info']:
            item['product_info']['brand'] = extract_brand(item['product_info']['brand'])

        return item

class SQLPipeline:
    def open_spider(self, spider):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="crawl_database"
        )
        
    def process_item(self, item, spider):
        cursor = self.db.cursor()

        column_names = (', '.join(item["product_info"].keys()) + ', image_path' + ', website')
        sql = f"""
            INSERT INTO {item["category"]} ({column_names}) 
            VALUES ({("%s," * (len(item["product_info"]) + 2)).strip(',')})
            ON DUPLICATE KEY UPDATE id=id
        """

        new_row = list(item["product_info"].values())

        if "image_paths" in item:
            for image_path in item["image_paths"]:
                new_row.append(image_path)
        else:
            new_row.append(None)
        
        new_row.append(item["website"])

        cursor.execute(sql, new_row)
        self.db.commit()
        
        return item

