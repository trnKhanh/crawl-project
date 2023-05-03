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
    found = re.search(r'\d+(\.\d*)?\s*GHz', cpu, re.IGNORECASE)
    if found:
        first_pos = found.start()
    else:
        first_pos = len(cpu)
    
    cpu = cpu[:first_pos].strip()
    return cpu


def extract_disk(disk):
    if not disk:
        return None

    in_bracket = re.search(r'\(.*\)', disk)
    if in_bracket:
        disk = disk.replace(in_bracket.group(), "")
    disk_type = re.search(r'SSD|HDD|EMMC', disk.upper())
    if disk_type:
        disk_type = disk_type.group()
    else:
        disk_type = "SSD"
    
    pattern = r'(?<=(SSD|HDD|EMMC)[^\S\n]*)\d+[^\S\n]*\w*?B'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        amount = extract_byte(amount)
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type
    
    pattern = r'\d+[^\S\n]*\w*?B(?=[^\S\n]*(SSD|HDD|EMMC))'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        amount = extract_byte(amount)
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type
    
    pattern = r'\d+\s*\w*?B'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        amount = extract_byte(amount)
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type
    
    return None

def extract_screen(screen):
    if not screen:
        return None
    
    result = re.search(r'\d+(\.\d+)?(?=.*?(inch|\'|\"|\”))', screen)
    if result:
        result = result.group()
        return result + ' inch'
    
    return None



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