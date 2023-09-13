def remove_numbers(string):
    return ''.join(char for char in string if not char.isdigit())
