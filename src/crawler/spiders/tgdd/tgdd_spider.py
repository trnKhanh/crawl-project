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
    filter_url = "https://www.thegioididong.com/Category/FilterProductBox?c=<cate_id>&priceminmax=0-1000000&pi=0"
    urls = [
        # 'https://www.thegioididong.com',
    ]
    category_urls = [
        # 'https://www.thegioididong.com/dong-ho-deo-tay',
        'https://www.thegioididong.com/laptop',
    ]
    post_data = urlencode({"IsParentCate": False, "IsShowCompare": True, "prevent": True})

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for url in self.category_urls:
            yield scrapy.Request(url=url, callback=self.category_parse)

    def parse(self, response):
        for link in response.xpath("//body/header/descendant::a/@href").getall():
            url = response.urljoin(link)
            if url[-4:] == '-ldp':
                url = url[:-4]
            if 'https://www.thegioididong.com' in url:
                yield scrapy.Request(url=url, callback=self.category_parse)

    def category_parse(self, response):
        category_box = response.xpath("//section[contains(@id,'categoryPage')]")
        if not category_box:
            return
        print(response.request.url)
        id = category_box.xpath("self::*/@data-id").get()
        url = self.filter_url.replace("<cate_id>", id)

        # request for product list using productFilter
        yield scrapy.Request(
            url=url,
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }, 
            body=self.post_data, 
            callback=self.filter_parse,
            meta={"request-more": 0}
        )

    def filter_parse(self, response):
        data = json.loads(response.text)
        products = HtmlResponse(url="https://www.thegioididong.com", body=data["listproducts"], encoding="utf-8")
        

        # find and follow to product pages
        for product_link in products.xpath("//li/a[1]/@href").getall():
            url = response.urljoin(product_link)
            yield scrapy.Request(url=url, callback=self.product_parse)

        # request more data from tgdd's database
        if not response.meta.get("request-more"):
            for pi in range(20, data["total"], 20):
                url=response.request.url.replace("pi=0", f"pi={int(pi/20)}")
                
                yield scrapy.Request(   
                    url=url,
                    method=response.request.method,
                    headers=response.request.headers,
                    body=response.request.body, 
                    callback=self.filter_parse,
                    meta={"request-more": 1}
                )
    
    def product_parse(self, response):
        product_box = response.xpath("//section[contains(@class, 'detail')]")
        if not product_box:
            return
        # id = int(product_box.xpath("self::*/@data-cate-id").get())
        id = int(product_box.xpath("self::*/@data-cate-id").get())
        parameter_list = [] # store name of parameter
        parameter_data = [] # store the data about corresponding parameter

        # product name
        name = response.xpath("//h1/text()").get()
        to_remove = re.search(r'[\\/()]', name)
        if to_remove:
            to_remove = to_remove.start()
        else:
            to_remove = len(name)
        name = name[:to_remove]
        parameter_list.append("name")
        parameter_data.append(name)

        # product price
        price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        # normalize product price to integer
        if price: 
            price = re.sub(r"\D", "", price)
        price = int(price)
        parameter_list.append("price")
        parameter_data.append(price)

        # parse product parameter
        if id in category_parameter:
            for parameter_name in category_parameter[id]:
                if parameter_name == "disk":
                    data = ', '.join(filter(None, map(extract_disk, product_box.xpath(parameter_xpath(category_parameter[id][parameter_name])).getall())))
                elif parameter_name == "ram":
                    data = product_box.xpath(parameter_xpath(category_parameter[id][parameter_name])).get()
                else:
                    data = ', '.join(product_box.xpath(parameter_xpath(category_parameter[id][parameter_name])).getall())
                parameter_list.append(parameter_name)
                parameter_data.append(data)
        # parse product url
        url = response.request.url
        parameter_list.append("url")
        parameter_data.append(url)
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
        
