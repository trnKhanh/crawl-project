import scrapy
import re
from scrapy.http import HtmlResponse
import json
from urllib.parse import urlencode
from .tgdd_utils import *
from .tgdd_data import *
import regex as re

class TgddSpider(scrapy.Spider):
    name = 'tgdd'
    urls = [
        'https://www.thegioididong.com/Category/FilterProductBox?c=44&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5698&o=7&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=4547&o=14&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=86&o=14&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5693&priceminmax=0-1000000&o=13&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=5697&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=522&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=42&o=17&priceminmax=0-1000000&pi=0',
        'https://www.thegioididong.com/Category/FilterProductBox?c=7077&o=17&priceminmax=0-1000000&pi=0',

    ]
    post_data = urlencode({"IsParentCate": False, "IsShowCompare": True, "prevent": True})

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(   
                url=url,
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }, 
                body=self.post_data, 
                callback=self.parse,
            )
        

    def parse(self, response):
        data = json.loads(response.text)
        products = HtmlResponse(url="https://www.thegioididong.com", body=data["listproducts"], encoding="utf-8")
        
        id = re.search(r'(?<=(c=))\d*', response.request.url)
        if id:
            id = int(id.group())
        else: 
            id = -1

        # find and follow to product pages
        for product_link in products.xpath("//li/a[1]/@href").getall():
            url = response.urljoin(product_link)
            yield scrapy.Request(url=url, callback=self.product_parse, meta={"id": id})

        # request more data from tgdd's database
        for pi in range(20, data["total"], 20):
            url=response.request.url.replace("pi=0", f"pi={int(pi/20)}")
            
            yield scrapy.Request(   
                url=url,
                method=response.request.method,
                headers=response.request.headers,
                body=response.request.body, 
                callback=self.parse,
            )

    def product_parse(self, response):
        product_box = response.xpath("//section[contains(@class, 'detail')]")
        if not product_box:
            return
        # id = int(product_box.xpath("self::*/@data-cate-id").get())
        id = response.meta.get("id")
        parameter_list = [] # store name of parameter
        parameter_data = [] # store the data about corresponding parameter

        # product name
        name = response.xpath("//h1/text()").get()
        parameter_list.append("name")
        parameter_data.append(f'"{name}"')

        # product price
        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        # normalize product price to integer
        if price: 
            price = re.sub(r"\D", "", price)
        parameter_list.append("price")
        parameter_data.append(price)

        # parse product parameter
        for parameter_name in category_parameter[id]:
            data = ', '.join(product_box.xpath(parameter_xpath(category_parameter[id][parameter_name])).getall())
            parameter_list.append(parameter_name)
            parameter_data.append(f"'{data}'")
        # parse product url
        url = response.request.url
        parameter_list.append("url")
        parameter_data.append(f"'{url}'")
        yield {
            "name": name
        }
        # add data to database
        sql = f"""
            INSERT INTO {get_category_table(id)} ({', '.join(parameter_list)}) 
            VALUES ({("%s," * len(parameter_list)).strip(',')})
            ON DUPLICATE KEY UPDATE id=id
        """
        crawl_cursor.execute(sql, parameter_data)
        crawl_db.commit()
        # follow the link to other products
        yield from self.product_follow(response)
    
    def product_follow(self, response):
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.product_parse, meta=response.meta)
        
