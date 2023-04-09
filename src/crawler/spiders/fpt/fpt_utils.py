import regex as re

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
vietnamese_charset = "àáâãèéêìíòóôõùúýỳỹỷỵựửữừứưụủũợởỡờớơộổỗồốọỏịỉĩệểễềếẹẻẽặẳẵằắăậẩẫầấạảđabcdeghiklmnopqrstuvxy0123456789"
def upper_text_xpath():
    return f"translate(text(), '{vietnamese_charset.lower()}','{vietnamese_charset.upper()}')"
def lower_text_xpath():
    return f"translate(text(),'{vietnamese_charset.upper()}','{vietnamese_charset.lower()}')"
def contain_word_xpath():
    return f'translate(text(),translate(text(),"{vietnamese_charset.upper()}{vietnamese_charset.lower()}",""),"")'
def parameter_xpath(parameter_name):
    parameter_name = parameter_name.lower()
    return f'(descendant-or-self::*[contains(concat(" ", normalize-space(@class), " "), " st-pd-table ") or contains(@class, "cttsktdetail") or contains(@class, "c-modal__content") or contains(@class,"detail-params")]/descendant::tr/*[1][descendant-or-self::*[contains({lower_text_xpath()}, "{parameter_name}")]])[1]/following-sibling::*[1]/descendant-or-self::*[{contain_word_xpath()}]/text()'

