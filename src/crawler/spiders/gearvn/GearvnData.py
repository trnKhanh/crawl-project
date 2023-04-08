type_product = {
    "Laptop" : 1,
    "Macbook": 1,
    "Màn hình" : 2,
    "GVN" : 3,
    "Bàn phím" : 4,
    "Chuột" : 5,
    "Tai nghe": 6,
    "Loa": 7,
    "Earphone": 8,
    "Tai nghe": 8,
    "Bộ định tuyến": 9,
    "Router": 10,
    "Webcam": 11,
    "SSD": 12,
    "HDD": 13,
    "Micro": 14,
    "Other" : 15,
}

alias_parameter = {
    "bandwidth": ["Băng tần mạng"],
    "brand": ["Thương hiệu", "Hãng sản xuất", "Nhà sản xuất", "Hãng"],
    "connect_type": ["Kiểu kết nối", "Kết nối", "Giao tiếp"],
    "compatible": ["Tương thích"],
    "compatible_micro": ["Tương thích", "Hệ điều hành"],
    "cpu": ["CPU"],
    "disk": ["Ổ lưu trữ", "Ổ cứng", "SSD", "HDD"],
    "dpi" : ["Độ nhạy", "Độ phân giải", "DPI"],
    "size_keyboard": ["Layout", "Số phím"],
    "size_screen": ["Kích thước"],
    "size_utils": ["Mức dung lượng"],
    "OS": ["Hệ điều hành"],
    "ram": ["RAM", "ram", "Ram"],
    "screen": ["Màn hình"],
    "type_earphone": ["Kiểu tai nghe"],
}

category_parameter = {
    type_product["Laptop"]: {
        "cpu": alias_parameter["cpu"],
        "disk": alias_parameter["disk"],
        "OS": alias_parameter["OS"],
        "ram": alias_parameter["ram"],
        "screen": alias_parameter["screen"],
    },
    type_product["GVN"]: {
        "cpu": ["CPU"],
        "ram": ["RAM"],
        "disk": ["SSD"],
        "OS": ["Hệ điều hành"],
    },
    type_product["Bàn phím"]: {
        "brand": alias_parameter["brand"],
        "compatible": alias_parameter["compatible"],
        "connect_type": alias_parameter["connect_type"],
        "size": alias_parameter["size_keyboard"],
    },
    type_product["Chuột"]: {
        "brand": alias_parameter["brand"],
        "connect_type": alias_parameter["connect_type"],
        "dpi": alias_parameter["dpi"],
    },
    type_product["Màn hình"]: {
        "screen_size": alias_parameter["size_screen"],
    },
    type_product["Tai nghe"]: {
        "brand": alias_parameter["brand"],
        "connect_type": alias_parameter["connect_type"],
        "type": alias_parameter["type_earphone"],
    },
    type_product["Loa"]: {
        "brand": alias_parameter["brand"],
        "connect_type": alias_parameter["connect_type"],
    },
    type_product["Bộ định tuyến"]: {
        "brand": alias_parameter["brand"],
        "bandwidth": alias_parameter["bandwidth"],
    },
    type_product["Webcam"]:{
        "brand": alias_parameter["brand"],
        "compatible": alias_parameter["compatible"],
    },
    type_product["Micro"]:{
        "brand": alias_parameter["brand"],
        "compatible": alias_parameter["compatible_micro"],
    },
    type_product["SSD"]:{
        "brand": alias_parameter["brand"],
        "size": alias_parameter["size_utils"],  
    },
    type_product["HDD"]:{
        "brand": alias_parameter["brand"],
        "size": alias_parameter["size_utils"],  
    },
    type_product["Other"]: {
        "brand": alias_parameter["brand"],
    }
}