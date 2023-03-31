from pathlib import Path

import scrapy

class GearvnSpider(scrapy.Spider):
    name = "gearvn"
    allowed_domains = ["gearvn.com"]
    def start_requests(self):
        urls = [
            'https://gearvn.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')