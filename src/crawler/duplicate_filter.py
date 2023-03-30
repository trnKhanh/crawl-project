import os
import json
from scrapy.dupefilters import RFPDupeFilter

class CustomFilter(RFPDupeFilter):
    urls_seen = set()

    def __del__(self):
        print("CustomFilter destruction")

    def request_seen(self, request):
        if request.url in self.urls_seen:
            return True
        else: 
            self.urls_seen.add(request.url)