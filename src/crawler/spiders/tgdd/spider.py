import scrapy
import re
from scrapy.http import HtmlResponse
import json
from urllib.parse import urlencode
from .tgdd_utils import *
from .data import *
import regex as re
from crawler.items import ProductItem

class TgddSpider(scrapy.Spider):
    name = 'tgdd'

    parameter_url = "https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={}&isAppliance=false&galleryType=5&colorId=0"
    
    urls = [
        'https://www.thegioididong.com',
    ]

    filter_url = "https://www.thegioididong.com/Category/FilterProductBox?c=<cate_id>&priceminmax=0-1000000&pi=0"
    post_data = urlencode({"IsParentCate": False, "IsShowCompare": True, "prevent": True})

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
            meta={"pi": 0}
        )

    def filter_parse(self, response):
        data = json.loads(response.text)
        products = HtmlResponse(url="https://www.thegioididong.com", body=data["listproducts"], encoding="utf-8")
    
        # find and follow to product pages
        for product in products.xpath("//li[contains(@class, 'item')]"):
            product_link = product.xpath("child::a[1]/@href").get()
            url = products.urljoin(product_link)

            thumb_image_url = product.xpath("descendant::img[contains(@class, 'thumb')]/@data-src").get()
            if thumb_image_url:
                thumb_image_url = products.urljoin(thumb_image_url)

            yield scrapy.Request(url=url, callback=self.product_parse, meta={"thumb_image_url": thumb_image_url})

        # request more data from tgdd's database
        cur_pi = response.meta.get("pi")

        if (cur_pi + 1) * 20 < data["total"]:
            url=response.request.url.replace("pi=0", f"pi={cur_pi+1}")
            
            yield scrapy.Request(   
                url=url,
                method=response.request.method,
                headers=response.request.headers,
                body=response.request.body, 
                callback=self.filter_parse,
                meta={"pi": cur_pi + 1}
            )
    
    def product_parse(self, response):
        # find product_box
        product_box = response.xpath("//section[contains(@class, 'detail')]")

        if not product_box:
            return
        # get product and category id
        category_id = int(product_box.xpath("self::*/@data-cate-id").get())
        product_id = int(product_box.xpath("self::*/@data-id").get())

        product_info = {}

        # product name
        name = product_box.xpath("//h1/text()").get()
        product_info["name"] = name

        # product price
        price = product_box.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        product_info["price"] = price
        
        # parse product url
        url = response.request.url
        product_info["url"] = url

        # pass image url down
        image_urls = [response.meta.get("thumb_image_url")]

        # parse product parameter
        yield scrapy.Request(url=self.parameter_url.format(product_id), 
                             callback=self.parameter_parse,
                             meta=dict(
                                category_id=category_id, 
                                image_urls=image_urls, 
                                product_info=product_info
        ))
        
        # follow the link to other products
        yield from self.follow_product(response)
    
    def follow_product(self, response):
        for next_page in response.xpath("(//*[@class='box03 group desk'])[1]/a/@href").getall():
            url = response.urljoin(next_page)
            yield scrapy.Request(url=url, callback=self.product_parse, meta=response.meta)

    def parameter_parse(self, response):
        product_info = response.meta.get("product_info")
        category_id = response.meta.get("category_id")

        if category_id in category_parameter:
            for parameter_name, name_in_web in category_parameter[category_id].items():
                data = ', '.join([s.strip() for s in response.xpath(parameter_xpath(name_in_web)).getall()])
                data = data.strip()
                if data.lower() in ['', 'hãng không công bố', 'không có']:
                    data = None
                product_info[parameter_name] = data

        category = get_category_table(category_id)
        image_urls = response.meta.get("image_urls")
        yield ProductItem(category=category, image_paths=image_urls, product_info=product_info, website="Thế giới di động")
