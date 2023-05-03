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
    
    return None

def extract_screen(screen):
    result = re.search(r'\d+(\.\d+)?\s*(inch|\')', screen)
    if result:
        result = result.group()
        return result
    
    return None

def extract_byte(data):
    pattern = r'\d+\s*\w*?B'
    amount = re.search(pattern, data.upper())
    if amount:
        return amount.group()
    return None




vietnamese_charset = "àáâãèéêìíòóôõùúýỳỹỷỵựửữừứưụủũợởỡờớơộổỗồốọỏịỉĩệểễềếẹẻẽặẳẵằắăậẩẫầấạảđabcdeghiklmnopqrstuvxy"
def upper_text_xpath():
    return f"translate(text(), '{vietnamese_charset.lower()}','{vietnamese_charset.upper()}')"
def lower_text_xpath():
    return f"translate(text(),'{vietnamese_charset.upper()}','{vietnamese_charset.lower()}')"
def contain_word_xpath():
    return f'translate(text(),translate(text(),"{vietnamese_charset.upper()}{vietnamese_charset.lower()}",""),"")'
def parameter_xpath(parameter_name):
    parameter_name = parameter_name.lower()
    return f'(descendant-or-self::*[contains(@id, "chitiet")]/descendant::tr/*[1][descendant-or-self::*[contains({lower_text_xpath()}, "{parameter_name}")]])[1]/following-sibling::*[1]/descendant::*[{contain_word_xpath()}]/text()'

def price_to_int(price):
    if price: 
        price = re.sub(r"\D", "", price)
        if price == '':
            price = None
        else:
            price = int(price)
        return price