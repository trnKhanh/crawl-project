type_product = {
    "Laptop" : 1,
    "Macbook": 1,
    "Màn hình" : 2,
    "GVN" : 3,
    "Bàn phím" : 4,
    "Chuột" : 5,
    "Tai nghe": 6,
    "Loa": 7,
    "Bộ định tuyến": 8,
    "Router": 8,
    "Other" : 9,
}

category_parameter = {
    type_product["Laptop"]: {
        "cpu": ["CPU"],
        "ram": ["RAM", "Ram"],
        "disk": ["Ổ lưu trữ", "Ổ cứng", "SSD"],
        "screen": ["Màn hình"],
        "OS": ["Hệ điều hành"],
    },
    type_product["GVN"]: {
        "cpu": ["CPU"],
        "ram": ["RAM"],
        "disk": ["SSD"],
        "OS": ["Hệ điều hành"],
    },
    type_product["Bàn phím"]: {
        "compatible": ["Tương thích"],
        "connect_type": ["Kết nối"],
        "size": ["Layout"],
        "brand": ["Thương hiệu"],
    },
    type_product["Chuột"]: {
        "dpi": ["Độ nhạy"],
        "connect_type": ["Kiểu kết nối"],
        "brand": ["Hãng sản xuất"],
    },
    type_product["Màn hình"]: {
        "screen_size": ["Kích thước"],
    },
    type_product["Tai nghe"]: {
        "connect_type": ["Kiểu kết nối", "Kết nối"],
        "type": ["Kiểu tai nghe"],
        "brand": ["Thương hiệu", "Hãng sản xuất"],
    },
    type_product["Loa"]: {
        "brand": ["Thương hiệu", "Hãng sản xuất"],
    },
    type_product["Bộ định tuyến"]: {
        "brand": ["Thương hiệu"],
        "bandwidth": ["Băng tần mạng"],
    },
    type_product["Other"]: {
        "brand": ["Thương hiệu", "Hãng sản xuất"]
    }
}