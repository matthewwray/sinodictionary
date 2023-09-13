def remove_numbers(string): #Remove numbers from a string
    return ''.join(char for char in string if not char.isdigit())