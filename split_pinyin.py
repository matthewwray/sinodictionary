def split_pinyin(string): #Original name: split_pinyin_with_numbers
    # def get_megalist():
    #     megalist = []
    #     with open('corresponding_pinyin.txt', 'r') as f:
    #         data = f.readlines()

    #     for element in data:
    #         element = element.replace('\n', '')
    #         element = element.split(':')
    #         for subelement in element:
    #             if subelement not in megalist:
    #                 subelement += '\n'
    #                 megalist.append(subelement)

    #     with open('megalist.txt', 'w',) as f:
    #         f.writelines(megalist)
    #         exit()
    #     return megalist

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
        x = get_first_pinyin_syllable(remaining_string, all_pinyin, 7)
        if x == 'INVALID':
            return 'INVALID'
        remaining_string = remaining_string[len(x):]
        split_pinyin.append(x)
    
    return split_pinyin

def get_first_pinyin_syllable(string, all_pinyin, max_length):
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



def remove_numbers_from_list(l): # Removes all entries from a list, which contain numbers. IMPORTANT: Removes the entries, not just the numbers from the entries

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

#x = 'zhèshìyígèměilìdexiàntiānrìluòdejǐngsè'
#x = 'zheshiyigemeilidexiatianriluodejing'
#x = 'zhe4 shi4 yi2 g e4 mei3 li4 dex ia4 tian1 ri4 lu o4de 5jin g3se4'
# x = 'san1 ge4 dai4 biao3'

# print(split_pinyin(x))