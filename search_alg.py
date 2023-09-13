import parser
from split_pinyin import split_pinyin
from detect_pinyin_type import detect_pinyin_type
from pinyin_converter import accent_to_numeric
from remove_numbers import remove_numbers

cdb = parser.parse_cedict()

# The search algorithm takes a search term, which can be Hanzi, Pinyin Numeric, Pinyin Accented
# or English, and returns search results.

def search_alg(input, lang='CHINESE'): # If no language is specified, we assume it is Chinese until we find out otherwise

    # Return nothing if there is an empty search term
    if len(input) == 0:
        return [[], 'CHINESE']

    def search_english(input):
        results = []
        # We first search for exact search terms (ie, word for word match), and then follow it with general search terms
        for result in match_english_exact(input):
            results.append(result)
        for result in match_english_general(input):
            temp = []
            temp.append(result)
            for sorted_result in sort_by_key_length(temp, 'english'): # We sort the results by the english length
                results.append(sorted_result)
        return results
    
    def search_pinyin(input_pinyin):
        pinyin_type = detect_pinyin_type(input_pinyin)
        results = []

        # If accented, we convert to numeric first. We never search accented pinyin
        if pinyin_type == 'ACCENTED':
            input_pinyin = accent_to_numeric(input_pinyin)
            pinyin_type = 'NUMERIC'
        
        # If neither accented nor numeric, we do a nontonal search
        if pinyin_type == 'NEITHER':
           for result in match_nontonal_pinyin(input_pinyin):
                results.append(result)
                 
        # Perform the numeric search
        if pinyin_type == 'NUMERIC':
            for result in match_numeric_pinyin(input_pinyin):
                results.append(result)
        
        return results

    returned_lang = 'CHINESE'
    results = []

    # Single hanzi search
    if (len(input) == 1) and (is_chinese_character(input)):
        results.append(match_chinese_string_1to1(input)) # As with English, first we do an exact, 1-to-1 search

        for result in match_chinese_string_phrase(input): #Then we match all the phrases that contain the character
            results.append(result)
    
    # Search full Chinese string
    elif is_chinese_string(input):
        results.append(match_chinese_string_1to1(input)) # Exactly match the full phrase
        
        for char in input:
            results.append(match_chinese_string_1to1(char)) # Then show results for each individual constituent character

        for result in match_chinese_string_phrase(input): #  For if the phrase is found within another larger string
            results.append(result)
    
    else: #Is either pinyin, or english. We need to find out which

        input_pinyin = split_pinyin(input) # Attempt to split the string as pinyin. If an INVALID response is returned, then we deduce the string is English
        if input_pinyin == 'INVALID':
            for result in search_english(input): # Perform the english search
                results.append(result)
                returned_lang = 'ENGLISH'

        else:
            # The string has been detected as valid pinyin. This doesn't necessarily mean the string is intended to be pinyin, however
            # For example the string 'women' is both valid pinyin and English. There are many more examples of this
            
            # We attempt a pinyin search IF lang is set to CHINESE. lang is set primarily by the C-E button next to the search bar
            if lang == 'CHINESE': 
                for result in search_pinyin(input_pinyin):
                    results.append(result)
            
            # If either the language is not chinese, or if no results were returned by the chinese search,
            # then we attempt an English search on the string
            if len(results) == 0: 
                for result in search_english(input):
                    results.append(result)
                    returned_lang = 'ENGLISH'

                # This particular Chinese search is useful in one use case:
                # The user has set the C-E button to E (English) but the string is in fact in Chinese (ie no English results). We override the C-E button
                if len(results) == 0: #If the English search returned no results, then search in Chinese
                    for result in search_pinyin(input_pinyin):
                        results.append(result)
                        returned_lang = 'CHINESE'


    return [sort_by_key_length(remove_none_from_list(results), 'english'), returned_lang] # We return our results, sorted by english def length, without empty results


# Below here is are the actual dictionary searching functions.
# They all essentially work the same way, iterate through the dictionary and select items that match whatever search term the functions take.

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


# Miscellaneous functions

def remove_none_from_list(l): #Remove all instances of None from a list
    new_list = []
    for element in l:
        if element != None:
            new_list.append(element)
    return new_list

def sort_by_key_length(lst, key):
    return sorted(lst, key=lambda x: len(x.get(key, "")))