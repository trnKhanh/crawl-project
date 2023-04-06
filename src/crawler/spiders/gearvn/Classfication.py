import re
from .GearvnData import *

def parse(name_product):
    for type in type_product:
        check = re.search(f"^{type}.*",name_product)
        if check:
            return type_product[type]
    return 8 #Unknown

def parse_following_type(type, response):
    dict = {}
    div = response.xpath('//div[@id="chitiet"]')[0]
    if type == 1:
        dict["CPU"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"CPU")]]]/child::*[2]/*/*/text()').get()
        dict["RAM"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"RAM")]]]/child::*[2]/*/*/text()').get()
        dict["Ổ lưu trữ"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Ổ lưu trữ")]]]/child::*[2]/*/*/text()').get()
        dict["Màn hình"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Màn hình")]]]/child::*[2]/*/*/text()').get()
        dict["Hệ điều hành"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Hệ điều hành")]]]/child::*[2]/*/*/text()').get()
        return dict
    if type == 2:
        dict["Kích thước"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Kích thước")]]]/child::*[2]/*/*/text()').get()
    if type == 3:
        dict["CPU"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"CPU")]]]/child::*[2]/*/*/text()').get()
        dict["RAM"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"RAM")]]]/child::*[2]/*/*/text()').get()
        dict["Ổ lưu trữ"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"SSD")]]]/child::*[2]/*/*/text()').get() + "," + div.xpath('descendant::*[td[descendant::*[contains(text(),"HDD")]]]/child::*[2]/*/*/text()').get()
        dict["Màn hình"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"CPU")]]]/child::*[2]/*/*/text()').get()
        dict["Hệ điều hành"] = "None"
        return dict
    if type == 4:
        dict["Tương thích"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Tương thích")]]]/child::*[2]/*/*/text()').get()
        dict["Kết nối"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Kết nối")]]]/child::*[2]/*/*/text()').get()
        dict["Layout"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Layout")]]]/child::*[2]/*/*/text()').get() + "," + div.xpath('descendant::*[td[descendant::*[contains(text(),"HDD")]]]/child::*[2]/*/*/text()').get()
        dict["Thương hiệu"] = div.xpath('descendant::*[td[descendant::*[contains(text(),"Thương hiệu")]]]/child::*[2]/*/*/text()').get()
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
