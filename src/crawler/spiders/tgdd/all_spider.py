from . import tgdd_spider
import re
from . import tgdd_utils
import scrapy

class AllSpider(tgdd_spider.TgddSpider):
    name = "tgdd_all"
    urls = [
        'https://www.thegioididong.com',
    ]
    forbidden = [
        "tien-ich",
        "game-app",
        "tin-tuc",
        "hoi-dap",
    ]
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def init_parse(self, response):
        for link in response.xpath("//a/@href").getall():
            url = response.urljoin(link)
            # normalize url
            url = url.split("?")[0].split("#")[0]
            cut_url = url.split("/")
            # if go too deep then skip url
            if len(cut_url) > 5:
                continue

            if len(cut_url) > 3:
                section = cut_url[3]
            else:
                section = None

            if "https://www.thegioididong.com" in url and section not in self.forbidden:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.xpath("//body/header/descendant::a/@href").getall():
            url = response.urljoin(link)
            yield {"url": url}
        # # product name
        # name = response.xpath("//h1/text()").get()
        # # product price
        # price = response.xpath("//*[contains(@class, 'box-price-present')]/text()").get()
        # # normalize product price to integer
        # if price: 
        #     price = re.sub(r"\D", "", price)
        # # parse product parameter
        # url = response.request.url
        # # yield result of the current product
        # if name and price:
        #     yield {
        #         "name": name,
        #         "price": price,
        #         "url": url
        #     }

        # follow the link to other products that not in header bar
        # for link in response.xpath("//body/*[not(self::header)][not(contains(@class, 'header-top-bar'))]/descendant::a/@href").getall():
        #     url = response.urljoin(link)
        #     # normalize url
        #     url = url.split("?")[0].split("#")[0]
        #     cut_url = url.split("/")
        #     # if go too deep then skip url
        #     if len(cut_url) > 5:
        #         continue

        #     if len(cut_url) > 3:
        #         section = cut_url[3]
        #     else:
        #         section = None
                
        #     if "https://www.thegioididong.com" in url and section not in self.forbidden:
        #         yield scrapy.Request(url=url, callback=self.parse)
        