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

#remap
category_id = {}
for id in category_table:
    category_id[category_table[id]] = id

category_parameter = {
    "phone":{
        "chip" : "chipset",
        "size": "display_size",
        "ram": "memory_internal",
        "disk": "storage",
        "OS": "os_version",
    },
    "laptop": {
        "cpu": "cpu",
        "disk": "o_cung_laptop",
        "OS": "os_version",
        "ram": "laptop_ram",
        "screen": "display_type",
    },
    "tablet":{
        "chip": "chipset",
        "ram": "memory_internal",
        "disk": "storage",
        "screen": "display_size",
        "OS": "os_version",
    },
    "PC": {
        "cpu": "cpu",
        "ram": "laptop_ram", #weird !!!
        "disk": "hdd_sdd",
        "screen": "display_size",
        "OS": "os_version",
    },
    "keyboard": {
        "brand": "phone_accessory_brands", #weird !!!
        "compatible": "banphim_tuong_thich",
        "connect_type": "banphim_cach_ket_noi",
        "size": "banphim_kich_thuoc",
    },
    "mouse": {
        "brand": "phone_accessory_brands",
        "connect_type": "banphim_cach_ket_noi", #weird !!!
        "dpi": "sensors",
    },
    "screen": {
        "screen_size": "monitor_size_man_hinh",
    },
    "smart_watch":{ 
        "brand": "phone_accessory_brands", #weird !!!
        "size_screen": "smart_watch_duong_kinh_mat"
    },
    "other":{
        "brand": "phone_accessory_brands",
    }
}