# Parses a CC-Cedict Chinese-English dictionary file ('cedict_ts.u8') into a list of python dictionaries with the keys 'traditional', 'simplified', 'pinyin', 'english'

def parse_cedict():
    with open('cedict_ts.u8', 'r') as f:
        data = f.readlines()

        #We add each parsed entry to this list
        dictionary_list = []

        for entry in data:
            #We need to remove the lines at the start that are commented out as these do not contain useful data. Also any entry with a length less than 3 is erroneous
            if entry[0] == '#':
                continue
            if len(entry) < 3:
                continue

            # First we reemove the trailing ' and \n at the end of each entry.
            entry = entry.rstrip('/')
            entry = entry.rstrip('\n')

            #Then we split the entry into:  Chinese (traditional, simplified, pinyin) and English. Later we will further split down Chinese into its constituent parts
            chinese, english = entry.split('/', 1)
            english = english.rstrip('/')

            #Split Chinese into Chinese (traditional, simplified) and Pinyin
            chinese, pinyin = chinese.split('[')
            pinyin = pinyin.rstrip('] ')

            #Split Chinese into Traditional and Simplified
            traditional, simplified = chinese.split(' ', 1)
            traditional = traditional.rstrip(' ')
            simplified = simplified.rstrip(' ')

            #Now we have: traditional, simplified, pinyin, english.
            #We create a dictionary out of these that we can then add to the dictionary_list
            dictionary = {}
            dictionary['traditional'] = traditional
            dictionary['simplified'] = simplified
            dictionary['pinyin'] = pinyin
            dictionary['english'] = english
            dictionary_list.append(dictionary)
        
        return dictionary_list