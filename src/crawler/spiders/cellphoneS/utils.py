import regex as re

def price_to_int(price):
    if price: 
        price = re.sub(r"\D", "", price)
        if price == '':
            return None
        price = int(price)
        return price

def extract_num_from_last(pattern):
    if pattern == None or pattern == "":
        return 0
    
    index = 0
    
    for i in pattern:
        if i.isdigit() == True:
            break
        index = index + 1
    
    result_string = pattern[index:]
    
    if result_string == "":
        return 0
    
    result = price_to_int(result_string)
    return result