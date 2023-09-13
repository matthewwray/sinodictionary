import parser
from split_pinyin import split_pinyin
from detect_pinyin_type import detect_pinyin_type
from pinyin_converter import accent_to_numeric
from remove_numbers import remove_numbers

cdb = parser.parse_cedict()

def search_alg(input, lang='CHINESE'):
    if len(input) == 0:
        return [[], 'CHINESE']

    def search_english(input):
        results = []
        for result in match_english_exact(input):
            results.append(result)
        for result in match_english_general(input):
            temp = []
            temp.append(result)
            for sorted_result in sort_by_key_length(temp, 'english'):
                results.append(sorted_result)
        return results
    
    def search_pinyin(input_pinyin):
        pinyin_type = detect_pinyin_type(input_pinyin)
        results = []

        if pinyin_type == 'ACCENTED':
            input_pinyin = accent_to_numeric(input_pinyin)
            pinyin_type = 'NUMERIC'
        
        if pinyin_type == 'NEITHER':
           for result in match_nontonal_pinyin(input_pinyin):
                results.append(result)
            ## A non-tonal search. This requires a unique, separate search of the database that ignores/matches all tones
        
        if pinyin_type == 'NUMERIC':
            for result in match_numeric_pinyin(input_pinyin):
                results.append(result)
        
        return results

    returned_lang = 'CHINESE'
    results = []
    if (len(input) == 1) and (is_chinese_character(input)):
        results.append(match_chinese_string_1to1(input)) #First we match a 1-1 match

        for result in match_chinese_string_phrase(input): #Then we match all the phrases that contain the character
            results.append(result)
    
    elif is_chinese_string(input):
        results.append(match_chinese_string_1to1(input))
        
        for char in input:
            results.append(match_chinese_string_1to1(char))

        for result in match_chinese_string_phrase(input):
            results.append(result)
    
    else: #Is either pinyin, or english.
        input_pinyin = split_pinyin(input)
        if input_pinyin == 'INVALID':
            for result in search_english(input):
                results.append(result)
                returned_lang = 'ENGLISH'

        else:
            if lang == 'CHINESE':
                for result in search_pinyin(input_pinyin):
                    results.append(result)
            if len(results) == 0: #If either the language is not chinese (by this point there would be no results), or if no results were returned by the chinese search
                for result in search_english(input):
                    results.append(result)
                    returned_lang = 'ENGLISH'
                if len(results) == 0: #If the English search returned no results, then search in Chinese
                    for result in search_pinyin(input_pinyin):
                        results.append(result)
                        returned_lang = 'CHINESE'


    return [sort_by_key_length(remove_none_from_list(results), 'english'), returned_lang]

def match_english_exact(string):
    results = []
    for entry in cdb:
        if string.lower() == entry['english'].lower():
            results.append(entry)
    return results

def match_english_general(string):
    string = string.lower()
    results = []
    for entry in cdb:
        if string in entry['english'].lower():
            results.append(entry)
    return results

def is_chinese_string(string):
    for char in string:
        if not is_chinese_character(char):
            return False
    return True

def is_chinese_character(char):
    # Check if the character falls within the Unicode range of Chinese characters
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False

def convert_numeric_pinyin_to_dict_format(pinyin):
    new_pinyin = ""
    for syllable in pinyin:
        new_pinyin += syllable + " "
    new_pinyin = new_pinyin[:-1] # Get rid of final space character
    return new_pinyin


def match_numeric_pinyin(string):
    results = []
    string = convert_numeric_pinyin_to_dict_format(string)

    for entry in cdb:
        if entry['pinyin'].lower() == string:
            results.append(entry)
    return results

def match_nontonal_pinyin(string):

    results = []
    string = convert_numeric_pinyin_to_dict_format(string)

    for entry in cdb:
        if remove_numbers(entry['pinyin'].lower()) == string:
            results.append(entry)
    return results

def match_chinese_string_1to1(string):
    for entry in cdb:
        if (entry['traditional'] == string) or (entry['simplified'] == string):
            return entry

def match_chinese_string_phrase(string):
    results = []
    for entry in cdb:
        if (string in entry['traditional']) or (string in entry['simplified']):
            if entry not in results:
                results.append(entry)
    return results

def remove_none_from_list(l): #Remove all instances of None from a list
    new_list = []
    for element in l:
        if element != None:
            new_list.append(element)
    return new_list

def sort_by_key_length(lst, key):
    return sorted(lst, key=lambda x: len(x.get(key, "")))


# result_list = search_alg('語言')
# result_list = search_alg('yu3yan2neng2    li4')
# print(remove_none_from_list(result_list))