import regex as re

def get_category_table(category):
    if re.search(r'\\bmáy tính xách tay\\b', category, re.IGNORECASE):
        return "laptop"
    elif re.search(r'\\bđiện thoại\\b', category, re.IGNORECASE):
        return "phone"
    elif re.search(r'\\bmáy tính bảng\\b', category, re.IGNORECASE):
        return "tablet"
    elif re.search(r'\\bmáy tính để bàn\\b', category, re.IGNORECASE):
        return "pc"
    elif re.search(r'\\bbàn phím\\b', category, re.IGNORECASE):
        return "keyboard"
    elif re.search(r'\\bchuột\\b', category, re.IGNORECASE):
        return "mouse"
    elif re.search(r'\\bmàn hình\\b', category, re.IGNORECASE):
        return "screen"
    elif re.search(r'\\bsmartwatch\\b', category, re.IGNORECASE):
        return "smart_watch"
    else:
        return "other"

category_parameter = {
    "laptop": {
        "cpu": "CPU",
        "ram": "Dung lượng RAM",
        "disk": "Ổ cứng",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    "pc": {
        "cpu": "CPU",
        "ram": "Dung lượng RAM",
        "disk": "Ổ cứng",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    "keyboard": {
        "compatible": "tương thích",
        "connect_type": "Loại bàn phím",
        "size": "Số phím", # FPT do not have this parameter
        "brand": "Thương hiệu",
    },
    "mouse": {
        "dpi": "Độ phân giải",
        "connect_type": "Loại chuột",
        "brand": "Thương hiệu",
    },
    "screen": {
        "screen_size": 'Màn hình',
    },
    "tablet": {
        "chip": "CPU",
        "ram": "RAM",
        "disk": "Bộ nhớ trong",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    "phone": {
        "chip": "CPU",
        "ram": "RAM",
        "disk": "Bộ nhớ trong",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    "smart_watch": {
        "screen": "Màn hình",
        "brand": "Thương hiệu",
    }
}