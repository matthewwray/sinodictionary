accented_char = ['ā', 'á', 'ǎ', 'à', 'ē', 'é', 'ě', 'è', 'ī', 'í', 'ǐ', 'ì', 
'ō', 'ó', 'ǒ', 'ò', 'ū', 'ú', 'ǔ', 'ù', 'ǖ', 'ǘ', 'ǚ', 'ǜ', 'Ā', 'Á', 'Ǎ', 
'À', 'Ē', 'É', 'Ě', 'È', 'Ī', 'Í', 'Ǐ', 'Ì', 'Ō', 'Ó', 'Ǒ', 'Ò', 'Ū', 'Ú', 'Ǔ', 
'Ù', 'Ǖ', 'Ǘ', 'Ǚ', 'Ǜ']

def detect_pinyin_type(pinyin): #Takes a list as input
    def string_contains_accented_char(string):
        for char in string:
            if char in accented_char:
                return True
        return False

    def string_contains_number(string):
        for char in string:
            if char.isdigit():
                return True
        return False

    for element in pinyin:
        if string_contains_number(element):
            return 'NUMERIC'
        elif string_contains_accented_char(element):
            return 'ACCENTED'
    return 'NEITHER'