# Takes pinyin lists generated from split_pinyin, and converts them
# Can convert bidirectionally from accented to numeric pinyin

def load_corresponding_pinyin():
    # This function loads a list of corresponding numeric and accented pinyin that can then be used to convert between the two
    with open('corresponding_pinyin.txt', 'r') as f:
        data = f.readlines()
    new_data = []
    for element in data:
        new_data.append(element.replace('\n','').split(':'))
    return new_data

def accent_to_numeric(pinyin_list):
    corresponding_list = load_corresponding_pinyin()

    numeric_pinyin_list = []
    for pinyin in pinyin_list:
        for value in corresponding_list:
            if value[1] == pinyin:
                numeric_pinyin_list.append(value[0])
                break
    return numeric_pinyin_list

def numeric_to_accent(pinyin_list):
    corresponding_list = load_corresponding_pinyin()

    numeric_pinyin_list = []
    for pinyin in pinyin_list:
        for value in corresponding_list:
            if value[0] == pinyin:
                numeric_pinyin_list.append(value[1])
                break
    return numeric_pinyin_list