# We must split a string of pinyin characters into separate pinyin units (syllables).
# Furthermore, we can use this process to deduce if a string is in English or Pinyin, because
# if an error occurs then the string is not valid pinyin and as such we can interpret it
# as English text.

def split_pinyin(string):
    # To split the pinyin, the process is as follows:
    # 1. Remove the spaces
    # 2. Iterate through the string, extracting valid pinyin syllables from the string
    # and storing them in a list
    # 3. If the string contains a part that is not valid pinyin, then it must be either 
    # non-pinyin text or invalid pinyin.

    def get_megalist():
        with open('megalist.txt', 'r') as f:
            return f.read().splitlines()
    
    def remove_spaces(string):
        new_string = ""
        for char in string:
            if char != ' ':
                new_string += char
        return new_string

    split_pinyin = []
    
    all_pinyin = get_megalist()

    remaining_string = remove_spaces(string)
    while remaining_string != "":
        # Next we get the first pinyin syllable from the string.
        # We then add this syllable to the list, chop off that syllable from the string,
        # and continue until there is no more text to be processed
        x = get_first_pinyin_syllable(remaining_string, all_pinyin, 7) #Longest pinyin syllable possible is 7, eg: 'zhuang1'

        if x == 'INVALID':
            return 'INVALID'
        
        remaining_string = remaining_string[len(x):]
        split_pinyin.append(x)
    
    return split_pinyin

def get_first_pinyin_syllable(string, all_pinyin, max_length):
    # This gets the first and longest possible pinyin syllable from the string provided. S
    # Supports both accented and numeric pinyin
    done = False
    remaining_length = len(string)

    while done == False:
        if max_length <= remaining_length:
            x = max_length
        else:
            x = remaining_length

        while x != 0:
            if string[:x] in all_pinyin:
                return string[:x]
            else:
                x -= 1
        if x == 0:
            return "INVALID"

def remove_numbers_from_list(l): # Removes all entries from a list, which contain numbers.

    def contains_number(string):
        for char in string:
            if char.isdigit():
                return True
        return False

    new_list = []
    for element in l:
        if not contains_number(element):
            new_list.append(element)
    return new_list