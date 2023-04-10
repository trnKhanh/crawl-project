import regex as re

# div.id
category_table = {
    "542lp90LP": "laptop",
    "YBPdfL8u8": "PC",
    "criteo-tags-div": "keyboard",
    "DneOAgAQr": "mouse",
    "duhUiJSKJ": "screen",
    "M_fpGirLP": "tablet",
    "9D9j1kQsZ": "phone",
    "Jv83PBoWm": "smart_watch"
}

def get_category_table(id):
    if id in category_table:
        return category_table[id]
    else:
        return "other"
    
alias_parameter = {
    "brand": ["Hãng sản xuất"],
    "connect_type": ["Cách kết nối", "Kết nối"],
    "compatible": ["Tương thích"],
    "cpu": ["CPU", "Loại CPU"],
    "chip": ["chipset"],
    "disk": ["Bộ nhớ trong", "Ổ cứng"],
    "dpi" : ["Độ phân giải"],
    "size_keyboard": ["Kích thước bàn phím"],
    "size_screen": ["Kích thước màn hình"],
    "os": ["Hệ điều hành"],
    "ram": ["Dung lượng Ram"],
    "screen": ["Màn hình"],
}

category_parameter = {
    "Phone":{
        "chip" : alias_parameter["chip"],
        "size": alias_parameter["size_screen"],
        "ram": alias_parameter["ram"],
        "disk": alias_parameter["disk"],
        "OS": alias_parameter["os"],
    },
    "Laptop": {
        "cpu": alias_parameter["cpu"],
        "disk": alias_parameter["disk"],
        "OS": alias_parameter["os"],
        "ram": alias_parameter["ram"],
        "screen": alias_parameter["screen"],
    },
    "PC": {
        "cpu": alias_parameter["cpu"],
        "ram": alias_parameter["ram"],
        "disk": alias_parameter["disk"],
        "screen": alias_parameter["size_screen"],
        "OS": alias_parameter["os"],
    },
    "Keyboard": {
        "brand": alias_parameter["brand"],
        "compatible": alias_parameter["compatible"],
        "connect_type": alias_parameter["connect_type"],
        "size": alias_parameter["size_keyboard"],
    },
    "Mouse": {
        "brand": alias_parameter["brand"],
        "connect_type": alias_parameter["connect_type"],
        "dpi": alias_parameter["dpi"],
    },
    "Screen": {
        "screen_size": alias_parameter["size_screen"],
    },
    "smart_watch":{ 
        "brand": alias_parameter["brand"],
        "size_screen": alias_parameter["size_screen"]
    },
    "Other": { 
        "brand": alias_parameter["brand"],
    }
}