import regex as re

def get_category_table(name):
    name = name.lower()
    if re.match(r'samsung.*', name):
        return "Phone"
    elif re.match(r'xiaomi.*', name):
        return "Laptop"
    elif re.match(r'iphone.*', name):
        return "Laptop"
    elif re.match(r'oppo.*', name):
        return "Keyboard"
    elif re.match(r'chuột.*', name):
        return "Mouse"
    elif re.match(r'màn hình.*', name):
        return "Screen"
    else:
        return "Other"
    
alias_parameter = {
    "brand": ["Thương hiệu", "Hãng sản xuất", "Nhà sản xuất", "Hãng"],
    "connect_type": ["Kiểu kết nối", "Kết nối", "Giao tiếp"],
    "compatible": ["Tương thích"],
    "cpu": ["CPU"],
    "chip": ["chipset"],
    "disk": ["Ổ lưu trữ", "Ổ cứng", "Bộ nhớ trong"],
    "dpi" : ["Độ nhạy", "Độ phân giải", "DPI"],
    "size_keyboard": ["Layout", "Số phím"],
    "size_screen": ["Kích thước màn hình"],
    "os": ["Hệ điều hành"],
    "ram": ["ram", "Dung lượng ram"],
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
    "Other": {
        "brand": alias_parameter["brand"],
    }
}