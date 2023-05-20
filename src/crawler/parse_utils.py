import regex as re

def extract_byte(data):
    if not data:
        return None
    pattern = r'\d+\s*\w*?B'
    amount = re.search(pattern, data.upper())
    
    if amount:
        amount = amount.group()
        number = re.search(r'\d+', amount)
        if number:
            number = number.group()
            return amount.replace(" ","").replace(number, number + " ")
    return None

def extract_cpu(cpu):
    if not cpu:
        return None
    
    cpu.replace(",","")
    found = re.search(r'\d+(\.\d*)?\s*GHz', cpu, re.IGNORECASE)
    if found:
        first_pos = found.start()
    else:
        first_pos = len(cpu)
    
    cpu = cpu[:first_pos].strip()
    return cpu

def extract_disk(disk_str):
    if not disk_str:
        return None
    # remove () bracket
    disks = disk_str.split(',')
    res = []
    for disk in disks:
        in_bracket = re.search(r'\(.*\)', disk)
        if in_bracket:
            disk = disk.replace(in_bracket.group(), "")

        # extract disk type (SSD, HHD, EMMC)
        disk_type = re.search(r'SSD|HDD|EMMC', disk.upper())
        if disk_type:
            disk_type = disk_type.group()
        else:
            disk_type = "SSD"
        
        # various pattern from observation on raw data
        patterns = [r'(?<=(SSD|HDD|EMMC)[^\S\n]*)\d+[^\S\n]*\w*?B',
                    r'\d+[^\S\n]*\w*?B(?=[^\S\n]*(SSD|HDD|EMMC))',
                    r'\d+\s*\w*?B']
        for pattern in patterns:
            amount = re.search(pattern, disk.upper())
            if amount:
                amount = amount.group()
                amount = extract_byte(amount)
                # amount = normalize_disk_amount(amount)
                if amount == None:
                    continue
                res.append(amount + ' ' + disk_type)
                break
            
    return ', '.join(res)

def extract_screen(screen):
    if not screen:
        return None
    
    result = re.search(r'\d+(\.\d+)?(?=.*?(inch|\'|\"|\”))', screen)
    if result:
        result = result.group()
        return result + ' inch'
    
    return None

def extract_price(price):
    if price: 
        price = re.sub(r"\D", "", price)
        if price == '':
            price = None
        else:
            price = int(price)
        return price
    else:
        return None

def extract_name(name):
    if not name:
        return None
    
    to_remove = re.search(r'[\\/()]', name)
    if to_remove:
        to_remove = to_remove.start()
    else:
        to_remove = len(name)

    name = name[:to_remove]
    name = name.strip()

    return name

def remove_extra(data):
    if not data:
        return None
    
    to_remove = re.search(r'[\\/()]', data)
    if to_remove:
        to_remove = to_remove.start()
    else:
        to_remove = len(data)

    data = data[:to_remove]
    data = data.strip()

    return data

def extract_brand(brand):
    return str(brand).split(', ')[0].strip('.').capitalize()

def normalize_disk_amount(amount):
    if amount == None:
        return None
    unit = re.search(r'[^\W\d]*B', amount)
    number = re.search(r'\d+', amount)
    if number == None or unit == None:
        return None
    number = int(number.group())
    unit = unit.group()
    return str(number * disk_unit_rate[unit]) + " B"

disk_unit_rate = {
    "B": 1,
    "KB": 1024,
    "MB": 1024*1024,
    "GB": 1024*1024*1024,
    "TB": 1024*1024*1024*1024,
}