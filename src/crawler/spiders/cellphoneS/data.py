import regex as re

# div.id
category_table = {
    3: "phone",
    380: "laptop",
    4: "tablet",
    665: "keyboard",
    664: "mouse",
    784: "screen",
    610: "smart_watch",
    864: "PC",
}

def get_category_table(id):
    if id in category_table:
        return category_table[id]
    else:
        return "other"

category_id = {}
for id in category_table:
    category_id[category_table[id]] = id

alias_parameter = {
    "brand": ["Hãng sản xuất"],
    "connect_type": ["Cách kết nối", "Kết nối"],
    "compatible": ["Tương thích"],
    "cpu": ["CPU", "Loại CPU"],
    "chip": ["chipset"],
    "disk": ["storage"],
    "dpi" : ["Độ phân giải"],
    "size_keyboard": ["Kích thước bàn phím"],
    "size_screen": ["display_size"],
    "os": ["operating_system"],
    "ram": ["memory_internal"],
    "screen": ["Màn hình"],
}

category_parameter = {
    category_id["phone"]:{
        "chip" : alias_parameter["chip"],
        "size": alias_parameter["size_screen"],
        "ram": alias_parameter["ram"],
        "disk": alias_parameter["disk"],
        "OS": alias_parameter["os"],
    },
    category_id["laptop"]: {
        "cpu": alias_parameter["cpu"],
        "disk": alias_parameter["disk"],
        "OS": alias_parameter["os"],
        "ram": alias_parameter["ram"],
        "screen": alias_parameter["screen"],
    },
    category_id["PC"]: {
        "cpu": alias_parameter["cpu"],
        "ram": alias_parameter["ram"],
        "disk": alias_parameter["disk"],
        "screen": alias_parameter["size_screen"],
        "OS": alias_parameter["os"],
    },
    category_id["keyboard"]: {
        "brand": alias_parameter["brand"],
        "compatible": alias_parameter["compatible"],
        "connect_type": alias_parameter["connect_type"],
        "size": alias_parameter["size_keyboard"],
    },
    category_id["mouse"]: {
        "brand": alias_parameter["brand"],
        "connect_type": alias_parameter["connect_type"],
        "dpi": alias_parameter["dpi"],
    },
    category_id["screen"]: {
        "screen_size": alias_parameter["size_screen"],
    },
    category_id["smart_watch"]:{ 
        "brand": alias_parameter["brand"],
        "size_screen": alias_parameter["size_screen"]
    },
}