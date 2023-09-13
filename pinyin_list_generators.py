import parser
from remove_numbers import remove_numbers

vowels = ['a', 'e', 'i', 'o', 'u', 'ü', 'A', 'E', 'I', 'O', 'U', 'Ü']

def fix_ncolon(string):
    string = string.replace('u:','ü')
    return string

def calculate_all_pinyin_combinations():
    all_pinyin = []

    cdb = parser.parse_cedict()
    for line in cdb:
        if (fix_ncolon(remove_numbers(line['pinyin']).lower()) not in all_pinyin) and (' ' not in line['pinyin']):
            current_pinyin = fix_ncolon(remove_numbers(line['pinyin']).lower())
            for i in range(0,6):
                if i == 0:
                    i = ''
                temp = current_pinyin + str(i)
                all_pinyin.append(temp)

    all_pinyin = sorted(all_pinyin)

    with open('all_pinyin_combinations.txt', 'w') as f:
        for pinyin in all_pinyin:
            f.writelines(pinyin)
            f.writelines('\n')

def get_last_vowel(string):
    reversed_string = string[::-1]  # Reverse the string
    for char in reversed_string:
        if char in vowels:
            return char
    return None

def has_vowel(string):

    for char in string:
        if char in vowels:
            return True

    return False

def generate_accented_vowel(vowel, tone):
    if (tone == 'none') or (tone == 'neutral'):
        return vowel

    if vowel == 'a':
        if tone == 'high':
            return 'ā'
        elif tone == 'rising':
            return 'á'
        elif tone == 'risingfalling':
            return 'ǎ'
        elif tone == 'falling':
            return 'à'

    elif vowel == 'e':
        if tone == 'high':
            return 'ē'
        elif tone == 'rising':
            return 'é'
        elif tone == 'risingfalling':
            return 'ě'
        elif tone == 'falling':
            return 'è'

    elif vowel == 'i':
        if tone == 'high':
            return 'ī'
        elif tone == 'rising':
            return 'í'
        elif tone == 'risingfalling':
            return 'ǐ'
        elif tone == 'falling':
            return 'ì'

    elif vowel == 'o':
        if tone == 'high':
            return 'ō'
        elif tone == 'rising':
            return 'ó'
        elif tone == 'risingfalling':
            return 'ǒ'
        elif tone == 'falling':
            return 'ò'

    elif vowel == 'u':
        if tone == 'high':
            return 'ū'
        elif tone == 'rising':
            return 'ú'
        elif tone == 'risingfalling':
            return 'ǔ'
        elif tone == 'falling':
            return 'ù'

    elif vowel == 'ü':
        if tone == 'high':
            return 'ǖ'
        elif tone == 'rising':
            return 'ǘ'
        elif tone == 'risingfalling':
            return 'ǚ​'
        elif tone == 'falling':
            return 'ǜ'

def convert_numeric_to_accented(pinyin):
    if pinyin[-1] == '1':
        tone = 'high'
        pinyin = pinyin[:-1]
    elif pinyin[-1] == '2':
        tone = 'rising'
        pinyin = pinyin[:-1]
    elif pinyin[-1] == '3':
        tone = 'risingfalling'
        pinyin = pinyin[:-1]
    elif pinyin[-1] == '4':
        tone = 'falling'
        pinyin = pinyin[:-1]
    elif pinyin[-1] == '5':
        tone = 'neutral'
        pinyin = pinyin[:-1]
    else:
        tone = 'none'

    # Generate the accented pinyin according to these rules https://www.pinyin.info/rules/where.html

    if not (has_vowel(pinyin)):
        return 'ERROR'

    if ('a' in pinyin):
        new_vowel = generate_accented_vowel('a', tone)
        pinyin = pinyin.replace('a', new_vowel)
        return pinyin

    if ('e' in pinyin):
        new_vowel = generate_accented_vowel('e', tone)
        pinyin = pinyin.replace('e', new_vowel)
        return pinyin
    
    if ('ou' in pinyin):
        new_vowel = generate_accented_vowel('o', tone)
        pinyin = pinyin.replace('o', new_vowel)
        return pinyin
    
    else:
        last_vowel = get_last_vowel(pinyin)
        new_vowel = generate_accented_vowel(last_vowel, tone)
        pinyin = pinyin.replace(last_vowel, new_vowel)
        return pinyin

def generate_corresponding_pinyin():
    corresponding = []

    with open('all_pinyin_combinations.txt', 'r') as f:
        data = f.readlines()
        for numeric in data:
            numeric = numeric.replace('\n','')
            accented = convert_numeric_to_accented(numeric)
            if accented == 'ERROR':
                accented = remove_numbers(numeric)
            current_correspond = numeric + ':' + accented + '\n'
            corresponding.append(current_correspond)
    
    with open('corresponding_pinyin.txt', 'w') as f:
        f.writelines(corresponding)

def calculate_all_pinyin_combinations_accented():
    with open('corresponding_pinyin.txt', 'r') as f:
        all_accented_pinyin = []
        data = f.read().split('\n')

    for element in data:
        if len(element) < 3:
            continue #Avoid errors with empty lines
        accented_pinyin = element.split(':')[1]
        accented_pinyin += '\n'
        all_accented_pinyin.append(accented_pinyin)
    
    with open('all_accented_pinyin_combinations.txt', 'w') as f:
        f.writelines(all_accented_pinyin)

        
    
#calculate_all_pinyin_combinations()
#generate_corresponding_pinyin()
#calculate_all_pinyin_combinations_accented()