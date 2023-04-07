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
    )

class TgddSpider(scrapy.Spider):
    custom_settings = dict(
        PLAYWRIGHT_ABORT_REQUEST=should_abort_request
    )
    name = 'fpt'
    urls = [
        "https://fptshop.com.vn/"
    ]
    category_urls = [
        # "https://fptshop.com.vn/may-tinh-xach-tay?trang=100",
        # "https://fptshop.com.vn/dien-thoai?trang=100",
        # "https://fptshop.com.vn/may-tinh-bang?trang=100",
        "https://fptshop.com.vn/may-tinh-de-ban?trang=100"
    ]
    product_urls = [
        # "https://fptshop.com.vn/dien-thoai/samsung-galaxy-s23-ultra",
        # "https://fptshop.com.vn/may-tinh-xach-tay/asus-tuf-gaming-fx506lhb-hn188w-i5-10300h",
        # "https://fptshop.com.vn/may-tinh-bang/samsung-galaxy-tab-s6-lite-2022",
        # "https://fptshop.com.vn/man-hinh/man-hinh-viewsonic-va2409-h-24-inch",
        # "https://fptshop.com.vn/phu-kien/ban-phim-bluetooth-logitech-k380",
        # "https://fptshop.com.vn/may-tinh-de-ban/pc-e-power-office-12",
        # "https://fptshop.com.vn/man-hinh/man-hinh-viewsonic-va2409-h-24-inch",
        # "https://fptshop.com.vn/phu-kien/chuot-khong-day-targus-w600",
        # "https://fptshop.com.vn/smartwatch/apple-watch-ultra-gps-cellular-49mm-alpine-loop-small",
        "https://fptshop.com.vn/may-tinh-de-ban/pc-frt-e-power-006"
    ]

    def start_requests(self):
        for url in self.category_urls:
            yield scrapy.Request(url=url, callback=self.category_parse, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", ".fplistpdbox > *:nth-child(2)")
                ],
            ))
        # for url in self.product_urls:
        #     yield scrapy.Request(url=url, callback=self.product_parse, meta=dict(
        #         playwright=True,
        #         playwright_page_methods=[
        #             PageMethod("wait_for_selector", "div.l-pd"),
        #             PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)"),
        #             PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a"),
        #             PageMethod("click", ".st-pd-table-viewDetail > a")
        #         ],
        #         name="name",
        #     ))

    def parse(self, response):
        for category in response.css(".section-box.st-cate .cate-box a"):
            url = response.urljoin(category.xpath("@href").get())
            yield scrapy.Request(url=url, callback=self.category_parse)


    def category_parse(self, response):
        category_box = response.css(".fplistpdbox > *:nth-child(2)")
        for product in category_box.xpath("child::*[contains(@class, 'product')]/*[contains(@class, 'product__info')]/h3/a"):
            product_link = product.xpath("@href").get()
            url = response.urljoin(product_link)
            yield scrapy.Request(url=url, callback=self.product_parse, meta=dict(
                playwright=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.l-pd"),
                    PageMethod("wait_for_selector", "ol.breadcrumb > li:nth-child(2)"),
                    PageMethod("wait_for_selector", ".st-pd-table-viewDetail > a"),
                    PageMethod("click", ".st-pd-table-viewDetail > a")
                ],
                name=product.xpath("text()").get(),
            ))
    def product_parse(self, response):
        product_box = response.css("div.l-pd")

        category_breadcrumb = " ".join(product_box.xpath("//*[contains(@class, 'breadcrumb-item')][not(contains(@class, 'active'))]/*/text()").getall())
        category = get_category_table(category_breadcrumb)

        product_info = {}

        name = response.meta.get("name")
        product_info["name"] = name

        price = product_box.css('.st-price-main').get()
        if price: 
            price = re.sub(r"\D", "", price)
            price = int(price)
        product_info["price"] = price

        url = response.request.url
        product_info["url"] = url

        image_urls = [product_box.xpath("descendant::div[normalize-space(@class)='st-slider']/descendant::*[img][1]/@data-src").get()]
        if category in category_parameter:
            for parameter_name, name_in_web in category_parameter[category].items():
                data = ', '.join(product_box.xpath(parameter_xpath(name_in_web)).getall())
                
                if data.lower() in ['']:
                    data = None
                product_info[parameter_name] = data
        
        yield ProductItem(category=category, image_urls=image_urls, product_info=product_info, website="FPT")

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

        
