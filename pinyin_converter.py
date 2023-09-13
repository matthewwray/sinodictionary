# Takes pinyin lists generated from split_pinyin, and converts them

def load_corresponding_pinyin():
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


# x = ['zhè', 'shì', 'yí', 'gè', 'měi', 'lì', 'de', 'xiàn', 'tiān', 'rì', 'luò', 'de', 'jǐng', 'sè']
# if (numeric_to_accent(accent_to_numeric(x))) == x:
#     print("OK")
# print(x)

#x = ['zhe4', 'shi4', 'yi2', 'ge4', 'mei3', 'li4', 'de', 'xia4', 'tian1', 'ri4', 'luo4', 'de5', 'jing3', 'se4']