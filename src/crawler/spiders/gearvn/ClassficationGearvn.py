import re
from .GearvnData import *

def parse(name_product):
    for type in type_product:
        check = re.search(f"^{type}.*",name_product)
        if check:
            return type_product[type]
    return type_product["Other"] #Unknown

def parse_following_type(type, response):
    dict = {}
    if type == type_product["Other"]:
        return dict
    div = response.xpath('//div[@id="chitiet"]')[0]
    level = [0*"/*", 1*"/*", 2*"/*", 3*"/*", 4*"/*", 5*"/*"]
    for pa in category_parameter[type]:
        dict[pa] = None
        for style in category_parameter[type][pa]:
            for i in level:
                case = div.xpath(f'descendant::*[td[descendant::*[contains(text(),"{style}")]]]/child::*[2]{i}/text()').get()
                if case != None:
                    dict[pa] = case
                    break
                case = div.xpath(f'descendant::*[td[contains(text(),"{style}")]]/child::*[2]{i}/text()').get()
                if case != None:
                    dict[pa] = case
                    break
            if dict[pa] != None:
                break
            
    return dict
