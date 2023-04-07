import re
from .GearvnData import *

def parse(name_product):
    for type in type_product:
        check = re.search(f"^{type}.*",name_product)
        if check:
            return type_product[type]
    return 9 #Unknown

def parse_following_type(type, response):
    dict = {}
    if type == 7:
        return dict
    div = response.xpath('//div[@id="chitiet"]')[0]
    level = ["/*", 2*"/*", 3*"/*", 4*"/*", 5*"/*"]
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
    if type == 5:
        dict["Hãng sản xuất"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Hãng sản xuất")]]]/child::*[2]/*/*/text()').get()
        dict["Kiểu kết nối"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Kiểu kết nối")]]]/child::*[2]/*/*/text()').get()
        dict["Độ nhạy (DPI)"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Độ nhạy(DPI)")]]]/child::*[2]/*/*/text()').get()
        return dict
    
    if type == 7:
        dict["Thương hiệu"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Thương hiệu")]]]/child::*[2]/*/*/text()').get()
        dict["Kiểu tai nghe"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Kiểu tai nghe")]]]/child::*[2]/*/*/text()').get()
        dict["Tương thích"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Tương thích")]]]/child::*[2]/*/*/text()').get()
        return dict
    return dict
    pass
