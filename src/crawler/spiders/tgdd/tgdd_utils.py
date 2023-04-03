import regex as re
import mysql.connector

def extract_disk(disk):
    if disk == None:
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
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type
    
    pattern = r'\d+[^\S\n]*\w*?B(?=[^\S\n]*(SSD|HDD|EMMC))'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type
    
    pattern = r'\d+\s*\w*?B'
    amount = re.search(pattern, disk.upper())
    if amount:
        amount = amount.group()
        # amount = normalize_disk_amount(amount)
        if amount == None:
            return None
        return amount + ' ' + disk_type

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
def parameter_xpath(parameter_name):
    return f'descendant-or-self::*[contains(@class, "parameter")]/descendant::li/*[descendant-or-self::*[contains(text(), "{parameter_name}")]]/following-sibling::*[1]/*/text()'

crawl_db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="crawl_database"
)
crawl_cursor = crawl_db.cursor()