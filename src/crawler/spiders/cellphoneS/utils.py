def price_to_int(pattern):
    result = 0
    for i in pattern:
        if i == ',':
            continue
        result = result * 10 + int(i)
    return result

def extract_num_from_last(pattern):
    index = 0
    
    if pattern == None:
        return ""
    for i in pattern:
        if i.isnumeric() == True:
            break
        index = index + 1
    result_string = pattern[index:]
    if result_string == "":
        return result_string
    result = price_to_int(result_string)
    return result