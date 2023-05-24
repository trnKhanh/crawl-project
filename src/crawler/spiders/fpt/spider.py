import scrapy
import re
from scrapy.http import HtmlResponse
import json
from urllib.parse import urlencode
from .fpt_utils import *
from .data import *
import regex as re
from crawler.items import ProductItem
from scrapy_playwright.page import PageMethod

def should_abort_request(request):
    if not re.search(r'.*fptshop.*', request.url):
        return True

    return (
        request.resource_type == "image"
        or ".jpg" in request.url
        or ".png" in request.url
    )

class FPTSpider(scrapy.Spider):
    custom_settings = dict(
        PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 5 * 60 * 1000, # 5 minutes
        PLAYWRIGHT_ABORT_REQUEST = should_abort_request
    )
    name = 'fpt'
    # root urls
    urls = [
        "https://fptshop.com.vn",
        "https://fptshop.com.vn/phu-kien",
        "https://fptshop.com.vn/xiaomi",
        "https://fptshop.com.vn/dien-gia-dung",
        "https://fptshop.com.vn/apple"
    ]
    # loadmore API of pc parts
    loadmore_url = "https://fptshop.com.vn/linh-kien/api/LoadMoreProduct?CateId=&PageIndex={}&SortID=4&ListFilter=&CateNameAscii=&Keyword="
    # used when testing
    category_urls = [
    ]
    product_urls = [
    ]
    def start_requests(self):
        # crawl root (contains categories' links)
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, meta=dict(playwright=True))
        # scrape "linh kien may tinh"
        # disabled for testing 
        yield scrapy.Request(url=self.loadmore_url.format(1), callback=self.loadmore_parse)

    # parse categories link from roots
    def parse(self, response):
        for category in response.xpath("//*[contains(@class, 'st-cate') or contains(@class, 'chapter-list') or contains(@class, 'characters home')]/descendant::a"):
            url = f'{response.urljoin(category.xpath("@href").get())}?trang=1000000'

            yield scrapy.Request(url=url, 
                                 callback=self.category_parse_type_1, 
                                 errback=self.to_type_2, 
                                 meta=dict(
                                    playwright=True,
                                    playwright_page_methods=[
                                        PageMethod("wait_for_selector", "div.fplistpdbox", timeout=10 * 1000, state='attached'),
                                    ]
            ))

    # errback when the page is not type 1 
    def to_type_2(self, failure):
        url = failure.request.url.split('?')[0]
        yield scrapy.Request(url=url, callback=self.category_parse_type_2, meta=dict(
            playwright=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "#keywordviewmore", timeout=10 * 1000, state='attached'),
            ]
        ))

    # this is used for categories such as laptop, phone, tablet,...
    def category_parse_type_1(self, response):
        print(response.request.url)
        for product in response.xpath("//*[contains(@class, 'product__info')]/h3/a"):
            product_link = product.xpath("@href").get()
            url = response.urljoin(product_link)
            yield scrapy.Request(url=url, callback=self.product_parse_type_1, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.l-pd", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "div.st-slider img", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a", timeout=10 * 1000, state='attached'),
                    PageMethod("click", ".st-pd-table-viewDetail > a")
                ],
                name=product.xpath("text()").get(),
            ))
    
    # this is used for categories such as accessories
    def category_parse_type_2(self, response):
        print(response.request.url)
        keyword = response.xpath("//*[contains(@id, 'keywordviewmore')]/@value").get()
        cateId = re.search(r'(?<=CateId:)\d*', keyword)
        if cateId:
            cateId = int(cateId.group())
        url = f"https://fptshop.com.vn/phu-kien/api/ViewmoreProduct?CateId={cateId}&PageIndex=1&PageSize=1000000&keyword={keyword}"
        
        yield scrapy.Request(url=url, callback=self.viewmore_parse)

    # this is used for categories such as pc parts (usually a callback function when sending requests to loadmore API)
    def category_parse_type_3(self, response):
        print("https://fptshop.com.vn/linh-kien")
        for product in response.xpath("//*[contains(@class, 'product__info')]/h3/a"):
            product_link = product.xpath("@href").get()
            url = response.urljoin(product_link)
            if "https://fptshop.com.vn/linh-kien/" not in url:
                continue
            yield scrapy.Request(url=url, callback=self.product_parse_type_2, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.detail-content", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "div.slider-gallery__main img", timeout=10 * 1000, state='attached'),
                ],
                name=product.xpath("text()").get(),
            ))
    
    # parse viewmore API when proccessing accessories
    def viewmore_parse(self, response):
        data = json.loads(response.text)
        category_box = HtmlResponse(url="https://fptshop.com.vn/", body=data['viewproduct'], encoding="utf-8")
        for product in category_box.xpath("descendant::*[contains(@class, 'product_info')]/a"):
            product_link = product.xpath("@href").get()
            url = response.urljoin(product_link)
            name = product.xpath("descendant::*[contains(@class, 'product_name')]/text()").get()
            
            yield scrapy.Request(url=url, callback=self.product_parse_type_1, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.l-pd", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "div.st-slider img", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a", timeout=10 * 1000, state='attached'),
                    PageMethod("click", ".st-pd-table-viewDetail > a")
                ],
                name=name,
            ))
    
    # parse loadmore API when proccessing pc parts
    def loadmore_parse(self, response):
        data = json.loads(response.text)
        category_box = HtmlResponse(url="https://fptshop.com.vn/", body=data['product'], encoding="utf-8")
        # send data to category_parse_type_3 to parse
        yield from self.category_parse_type_3(category_box)

        page_id = re.search(r'(?<=PageIndex=)\d*',response.request.url)
        if page_id:
            page_id = int(page_id.group())
        else:
            page_id = 0

        # if there are more products, request more
        if data['totalrest'] > 0:
            yield scrapy.Request(url=self.loadmore_url.format(page_id + 1), callback=self.loadmore_parse)
    
    # parse products in laptop, phone, tablet, accessories, e.t.c
    def product_parse_type_1(self, response):
        product_box = response.css("div.l-pd")

        if "from_follow" not in response.meta and product_box.xpath("descendant::*[contains(concat(' ', normalize-space(@class),' '), ' st-select ')]/*"):
            yield from self.follow_product(response)
            return
        # parse category
        category_breadcrumb = "/".join(product_box.xpath("//*[contains(@class, 'breadcrumb-item')][not(contains(@class, 'active'))]/*/text()").getall())
        category = get_category_table(category_breadcrumb)

        product_info = {}
        # parse product name
        name = response.meta.get("name")
        if not name:
            name = product_box.xpath("descendant::*[contains(@class, 'st-name')]/text()").get()
        name = name.strip()

        product_info["name"] = name
        # parse and normalize price
        price = product_box.xpath('descendant::*[contains(@class, "st-price-main")]/text()').get()
        product_info["price"] = price

        url = response.request.url
        product_info["url"] = url
        # parse image url of product
        image_urls = [product_box.xpath("descendant::div[contains(concat(' ', normalize-space(@class),' '), ' st-slider ')]/descendant::*[not(contains(@class, 'st-slider__promo-box'))]/descendant::img[1]/@src").get()]
        
        # parse detail parameters
        if category in category_parameter:
            for parameter_name, name_in_web in category_parameter[category].items():
                data = ', '.join([s.strip() for s in product_box.xpath(parameter_xpath(name_in_web)).getall()])
                product_info[parameter_name] = data

        yield ProductItem(category=category, image_paths=image_urls, product_info=product_info, website="FPT")

        yield from self.follow_product(response)

    # parse products in pc parts
    def product_parse_type_2(self, response):
        product_box = response.css("div.detail-content")

        category_breadcrumb = " ".join(product_box.xpath("//*[contains(@class, 'breadcrumb-item')][not(contains(@class, 'active'))]/*/text()").getall())
        category = get_category_table(category_breadcrumb)

        product_info = {}

        name = response.meta.get("name").strip()
        product_info["name"] = name

        price = product_box.xpath('descendant::*[contains(@id, "product-price-online")]/text()').get()
        product_info["price"] = price

        url = response.request.url
        product_info["url"] = url

        image_urls = [product_box.xpath("descendant::div[contains(concat(' ', normalize-space(@class),' '), ' slider-gallery__main ')]/descendant::img[1]/@src").get()]
        if category in category_parameter:
            for parameter_name, name_in_web in category_parameter[category].items():
                data = ', '.join([s.strip() for s in product_box.xpath(parameter_xpath(name_in_web)).getall()])
                product_info[parameter_name] = data
        
        yield ProductItem(category=category, image_paths=image_urls, product_info=product_info, website="FPT")
    
    def follow_product(self, response):
        for product in response.xpath("descendant::*[contains(concat(' ', normalize-space(@class),' '), ' st-select ')]/*"):
            url = response.urljoin(product.xpath("@href").get())
            yield scrapy.Request(url=url, callback=self.product_parse_type_1, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.l-pd", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "div.st-slider img", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)", timeout=10 * 1000, state='attached'),
                    PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a", timeout=10 * 1000, state='attached'),
                    PageMethod("click", ".st-pd-table-viewDetail > a")
                ],
                name=None,
                from_follow=1,
            ))
        pass

        
