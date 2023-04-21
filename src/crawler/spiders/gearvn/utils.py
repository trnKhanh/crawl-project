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

def price_to_int(pattern):
    result = 0
    
    if pattern == None or pattern == "":
        return result
    
    for i in pattern:
        if not i.isdigit():
            continue
        result = result * 10 + int(i)
        
    return result