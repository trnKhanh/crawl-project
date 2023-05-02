import scrapy
import json
from .data import *
from .utils import *
from crawler.items import ProductItem

class CellphoneSSpider(scrapy.Spider):
    name = 'CellPhoneS_spider'
    start_urls = ['https://cellphones.com.vn/']

    api_category_url = "https://api.cellphones.com.vn/v2/graphql/query"
    
    thumbnail_url_prefix = "https://cdn2.cellphones.com.vn/358x358,webp,q100/media/catalog/product"
    
    hiden_category_urls = [
        'https://cellphones.com.vn/man-hinh.html',
        'https://cellphones.com.vn/phu-kien/chuot-ban-phim-may-tinh/ban-phim.html',
        'https://cellphones.com.vn/phu-kien/chuot-ban-phim-may-tinh/chuot.html',
    ]
    
    forbidden_urls = [
        'https://cellphones.com.vn/sforum/',
        'https://cellphones.com.vn/danh-sach-khuyen-mai',
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
            )
            
    def parse(self, response):
        category_box = response.xpath('descendant::div[contains(@class, "menu-tree")]/*/@href').getall()
        
        for link in category_box:
            if link == "#" or (link in self.forbidden_urls):
                continue
            yield scrapy.Request(
                url=link,
                method="POST",
                callback=self.parse_category,
            )
        #parse more
        for url in self.hiden_category_urls:
            yield scrapy.Request(
                url=url,
                method="POST",
                callback=self.parse_category
            )
        
    def parse_category(self, response):
        url = response.request.url

        query = """
query{
    products(
            filter: {
                static: {
                    categories: ["<cate-id>"],
                    province_id: 30, 
                    stock: {
                        from: 0
                    },
                    stock_available_id: [46, 56, 152],
                    filter_price: {from:0to:1000000000}
                },
                dynamic: {
                    
                }
            },
            page: 1,
            size: 10000,
            sort: [{view: desc}]
        )
    {
        general{
            product_id
            name
            attributes
            attributes
            sku
            doc_quyen
            manufacturer
            url_key
            url_path
            categories{
                categoryId
            }
        },
        filterable{
            is_installment
            stock_available_id
            filter {
                id
                Label
            }
            price
            special_price
            promotion_information
            thumbnail
            promotion_pack
            sticker
        },
    }
}"""
        
        category_info = response.xpath('descendant::div[contains(@class, "cps-container cps-body")]/*[2]/*[1]/@class').get()
        category_table = extract_num_from_last(category_info)

        yield scrapy.Request(
            url=self.api_category_url, 
            method="POST",
            callback=self.parse_product,
            headers={
                "Content-Type": "application/json",
            },
            meta=dict(
                category_url=url,
                category_id=category_table
            ),
            body=json.dumps({
                "query": query.replace("<cate-id>", "{}".format(category_table)),
                "variables": {},
            })
        )
        
    def parse_product(self, response):
        data = json.loads(response.body)
        data = data["data"]["products"]
        
        if data == None:
            return
        
        size = len(data)
        category_url = response.meta.get("category_url")[:-5]
        id = response.meta.get("category_id")
        
        for i in range(0, size):
            general = data[i]['general']
            filter = data[i]['filterable']
            attributes = general['attributes']
            
            url_thumbnail_product = [self.thumbnail_url_prefix + filter['thumbnail']]
            url_product = category_url + "/" + general["url_path"]
            name_product = general['name']  
            price = filter['special_price']
            
            info={
                "name" : name_product,
                "price" : price,
                "url" : url_product,
            }
            
            # print(name_product)
            for product_parameter, alias in category_parameter[get_category_table(id)].items():
                info[product_parameter] = None
                if alias not in attributes:
                    continue
                specify_info = attributes[alias]
                if specify_info != None:
                    info[product_parameter] = specify_info
                
            yield ProductItem(category=get_category_table(id),
                          image_urls=url_thumbnail_product,
                          product_info=info,
                          website="CellPhoneS")
            
    