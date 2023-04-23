def price_to_int(pattern):
    result = 0
    
    if pattern == None or pattern == "":
        return result
    
    for i in pattern:
        if not i.isdigit():
            continue
        result = result * 10 + int(i)
        
    return result

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