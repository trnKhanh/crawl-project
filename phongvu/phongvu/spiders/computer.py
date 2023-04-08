import scrapy


class ComputerSpider(scrapy.Spider):
    name = "computer"
    allowed_domains = ["phongvu.vn"]
    start_urls = ["https://phongvu.vn/c/laptop"]

    def parse(self, response):
        title = response.xpath('//h3[@class="css-1xdyrhj"]/@title').get()
        yield {'title': title}