category_table = {
    44: "laptop",
    5698: "PC",
    4547: "keyboard",
    86: "mouse",
    5697: "screen",
    522: "tablet",
    42: "phone",
    7077: "smart_watch"
}
def get_category_table(id):
    if id in category_table:
        return category_table[id]
    else:
        return "misc"
    
category_id = {}
for id in category_table:
    category_id[category_table[id]] = id

category_parameter = {
    category_id["laptop"]: {
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Ổ cứng",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    category_id["PC"]: {
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "Ổ cứng",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    category_id["keyboard"]: {
        "compatible": "Tương thích",
        "connect_type": "Cách kết nối",
        "size": "Số phím",
        "brand": "Hãng",
    },
    category_id["mouse"]: {
        "dpi": "Độ phân giải",
        "connect_type": "Cách kết nối",
        "brand": "Hãng",
    },
    category_id["screen"]: {
        "screen_type": 'Loại màn hình',
        "screen_size": 'Màn hình',
    },
    category_id["tablet"]: {
        "chip": "Chip",
        "ram": "RAM",
        "disk": "Dung lượng lưu trữ",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    category_id["phone"]: {
        "chip": "Chip",
        "ram": "RAM",
        "disk": "Dung lượng lưu trữ",
        "screen": "Màn hình",
        "OS": "Hệ điều hành",
    },
    category_id["smart_watch"]: {
        "screen": "Màn hình",
        "brand": "Hãng",
    }
}