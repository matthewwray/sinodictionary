import customtkinter
from PIL import Image, ImageTk
from search_alg import search_alg
from pinyin_converter import numeric_to_accent
from split_pinyin import split_pinyin
from pathlib import Path
from time import time
from datetime import datetime

# This is a graphical Chinese dictionary program made using customtkinter
# There is a main frame, App, which contains the Dictionary frame and the Sidebar frame.
# In turn, the Sidebar frame contains a few buttons, 
# and the Dictionary frame contains the Searchbar frame and the Results frame.
# When the search button is pressed it takes the search term in the search bar, searches and populates the results frame with the results.

# Firstly, if there is no config file then we create one with the default values
if not Path("config.ini").is_file():
    with open('config.ini', 'a+') as f:
        f.write("search_results_max = 30\nhistory_entries_max = 100\npinyin_type = Accented pinyin tones\ntheme = Dark mode\ncharacter_type = Simplified")

# Also we need to create a history file but we don't want anything in it
if not Path("history.csv").is_file():
    with open('history.csv', 'w') as f:
        pass

def write_history(entry): # Write a search entry to the history file
    htime = str(int(time()))
    entry = entry + ',' + htime + ',' + '\n'
    # Get all the current data in the history file. We will eventually add our new entry at the start of the list
    with open('history.csv', 'r') as hfile:
        hdata = hfile.readlines()

    # If the history file contains more entries than the maximum specifies is allowed, then we delete the oldest entries
    while len(hdata) >= get_field_from_config("history_entries_max"):
        del hdata[len(hdata)-1]

    hdata = [entry] + hdata

    with open('history.csv', 'w') as hfile:
        hfile.write(str(''.join(hdata)))
    
def get_history():
    with open('history.csv', 'r') as hfile:
        hdata = hfile.readlines()
    
    for i in range(len(hdata)):
        hdata[i] = hdata[i].split(',')
    
    return hdata

def get_field_from_config(field): # Get a value from the config file. field can be: search_result_max, history_entries_max, pinyin_type, theme, character_type
    with open('config.ini', 'r') as f:
        config = f.readlines()
        temp = []

        for c in config:
            c = c.split(' = ')[1]
            c = c.replace('\n','')
            temp.append(c)
        config = temp  

        if field == "search_results_max":
            return int(config[0])
    
        if field == "history_entries_max":
            return int(config[1])

        if field == "pinyin_type":
            return config[2]

        if field == "theme":
            return config[3]

        if field == "character_type":
            return config[4]

    raise ValueError("Invalid value read request to config")

def fix_ncolon(string): # Convert the unsightly u: into a more attractive form ü
    string = string.replace('u:','ü')
    return string

def remove_non_alphanumeric(string): # Removes non alpha-numeric chars from a string
    new_string = ""
    valid_chars= [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', 'ü',
    'Ü']
    for char in string:
        if char in valid_chars:
            new_string += char
    return new_string
    
class SidebarFrame(customtkinter.CTkFrame): # This frame only contains a few buttons
    def __init__(self, master):
        super().__init__(master)
        
        self.simple_characters = True

        self.appearance_mode = "dark"

        self.moon_graphic = customtkinter.CTkImage(Image.open("graphic/moon-90.png"))
        self.sun_graphic = customtkinter.CTkImage(Image.open("graphic/sun-100.png"))
        self.settings_graphic = customtkinter.CTkImage(Image.open("graphic/setting-100.png"))
        self.traditional_graphic = customtkinter.CTkImage(Image.open("graphic/traditional.png"))
        self.simplified_graphic = customtkinter.CTkImage(Image.open("graphic/simplified.png"))
        self.history_graphic = customtkinter.CTkImage(Image.open("graphic/history-100.png"))
        #self.camera_graphic = customtkinter.CTkImage(Image.open("graphic/camera-100.png"))

        self.settings_button = customtkinter.CTkButton(self, image=self.settings_graphic, text="", command=self.setting_button_callback, width=64, height=64)
        self.settings_button.grid(row=0, column=0, padx=15, pady=10, sticky="ewns")

        self.appearance_mode_button = customtkinter.CTkButton(self, image=self.moon_graphic, text="", command=self.appearance_mode_button_callback, width=64, height=64)
        self.appearance_mode_button.grid(row=1, column=0, padx=15, pady=(15,10), sticky="ewns")

        self.simplified_characters_button = customtkinter.CTkButton(self, image=self.simplified_graphic, text="", command=self.simple_characters_button_callback, width=64, height=64)
        self.simplified_characters_button.grid(row=2, column=0, padx=15, pady=10, sticky="ewns")

        self.history_button = customtkinter.CTkButton(self, image=self.history_graphic, text="", command=self.history_button_callback, width=64, height=64)
        self.history_button.grid(row=3, column=0, padx=15, pady=10, sticky="ewns")

        #self.camera_button = customtkinter.CTkButton(self, image=self.camera_graphic, text="", command=self.nothing, width=64, height=64)
        #self.camera_button.grid(row=4, column=0, padx=15, pady=10, sticky="ewns")
    
    def nothing(self):
        pass

    def setting_button_callback(self):
        app.create_settings_frame()

    def history_button_callback(self):
        app.create_history_frame()

    def simple_characters_button_callback(self): # Toggle between simple and traditional characters
        if self.simple_characters == True:
            self.simple_characters = False
            self.simplified_characters_button.configure(image=self.traditional_graphic)
        
        else:
            self.simple_characters = True
            self.simplified_characters_button.configure(image=self.simplified_graphic)

    def appearance_mode_button_callback(self): # Toggle between light and dark mode
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"
            self.appearance_mode_button.configure(image=self.sun_graphic)
        else:
            self.appearance_mode = "dark"
            self.appearance_mode_button.configure(image=self.moon_graphic)
        customtkinter.set_appearance_mode(self.appearance_mode)

class SearchbarFrame(customtkinter.CTkFrame): # Contains the language toggle (C-E) button, the search bar and the search button.
    def __init__(self, master):
        super().__init__(master)
        
        self.MAX_RESULTS = get_field_from_config("search_results_max") # If this number is too high, the dictionary becomes too unresponsive. 30 is sort of a sweet spot
        self.current_language = 'CHINESE'

        self.search_graphic = customtkinter.CTkImage(Image.open("graphic/search-50.png"))
        self.language_toggle_chinese_graphic = customtkinter.CTkImage(Image.open("graphic/c-50.png"))
        self.language_toggle_english_graphic = customtkinter.CTkImage(Image.open("graphic/e-50.png"))

        self.grid_columnconfigure(1, weight=1)

        self.language_toggle_button = customtkinter.CTkButton(self, image=self.language_toggle_chinese_graphic, command=self.toggle_language, text="", width=64, height=60)
        self.language_toggle_button.grid(row=0, column=0, padx=(10,10), pady=10, sticky="w")

        self.textbox = customtkinter.CTkEntry(self, font=("Calibri",26))
        self.textbox.grid(row=0, column=1, padx=(10,0), pady=10, ipady=10, sticky="ew")
        self.textbox.bind("<Return>", self.pressed_enter)

        self.search_button = customtkinter.CTkButton(self, image=self.search_graphic, text="", command=self.search_button_callback, width=64, height=60)
        self.search_button.grid(row=0, column=2, padx=(10,10), pady=10, sticky="e")

    def toggle_language(self): #  C-E button function
        if self.current_language == 'CHINESE':
            self.set_language('ENGLISH')
        else:
            self.set_language('CHINESE')
    
    def set_language(self, lang): # Settle the language specifically (ie, don't toggle but just set)
        if lang == 'CHINESE':
            self.current_language = lang
            self.language_toggle_button.configure(image=self.language_toggle_chinese_graphic)
        elif lang == 'ENGLISH':
            self.current_language = lang
            self.language_toggle_button.configure(image=self.language_toggle_english_graphic)

    def get_search(self): # Search button function
        app.dictionary_frame.results_frame.clear_results()
        app.dictionary_frame.refresh_results_frame()

        search = self.textbox.get()

        write_history(search) # Here we add the search to our history file

        search_results, returned_search_lang = search_alg(search, self.current_language)
        search_results = search_results[0:self.MAX_RESULTS]
        
        self.set_language(returned_search_lang)

        if app.sidebar_frame.simple_characters == True: # Check if we are set to use traditional or simplified characters for showing the results
            writing_system = 'simplified'
        else:
            writing_system = 'traditional'
        for result in search_results:
            app.dictionary_frame.results_frame.add_result(result[writing_system], result['pinyin'], result['english'])

    #Can either press search or press the search button to get results.
    def pressed_enter(self, event):
        self.get_search()
    
    def search_button_callback(self):
        self.get_search()

class ResultsFrame(customtkinter.CTkScrollableFrame): # This frame is populated with results when a search from the searchbar is triggered
    def __init__(self, master):
        super().__init__(master)

        self.results=[]
        self.grid_columnconfigure(0, weight=1)

    def add_result(self, chinese, pinyin, english): # Add a single result. Has a field for each attribute of the CC-CEDICT dictionary
        SingleResult = SingleResultFrame(self, chinese, pinyin, english)
        SingleResult.grid(row=len(self.results), column=0, padx=10, pady=10, sticky="we")
        self.results.append(SingleResult)

    def clear_results(self):
        for result in self.results:
            result.destroy()
        self.results = []

class SingleResultFrame(customtkinter.CTkFrame): # A frame for a single result. Many of these populate a single results frame
    def __init__(self, master, chinese, pinyin, english):
        super().__init__(master)

        self.chinese = chinese
        self.pinyin = pinyin.lower()
        self.english = english

        self.pinyin = fix_ncolon(self.pinyin)
        self.pinyin = remove_non_alphanumeric(self.pinyin)
        
        self.pinyin.replace("'",'')

        if get_field_from_config("pinyin_type") == "Numeric pinyin tones":
            self.pinyin = ''.join(split_pinyin(self.pinyin))
        else:
            self.pinyin = ''.join(numeric_to_accent(split_pinyin(self.pinyin)))

        self.grid_rowconfigure((0), weight=0)

        self.chinese_display = customtkinter.CTkLabel(self, text=self.chinese, font=("Calibri",24), wraplength=170, justify='left', width=170, anchor='w') # 是
        self.chinese_display.grid(row=0, column=0, padx=(10, 20), pady=(5,0), sticky="w")

        self.pinyin_display = customtkinter.CTkLabel(self, text=self.pinyin, font=("Calibri",16), wraplength=170, justify='left', anchor='w')
        self.pinyin_display.grid(row=1, column=0, padx=10, pady=(0,5), sticky="w")

        # The wraplength here gets the frame width so as to stop the text from going offscreen when it is long. When the window is resized to not be fullscreen, sometimes it will do this anyway, which the -240 fixes.
        self.english_display = customtkinter.CTkLabel(self, text=self.english, font=("Calibri",16), wraplength= app.dictionary_frame.get_results_frame_width()-240, justify='left', anchor='w')
        self.english_display.grid(row=0, column=1, padx=10, pady=5, sticky="w", rowspan=2)

class App(customtkinter.CTk): # The main frame. All other frames are contained within this frame
    def __init__(self):
        super().__init__()

        self.title("Chinese Dictionary")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = SidebarFrame(self)
        self.sidebar_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")
    
        self.dictionary_frame = DictionaryFrame(self)
        self.dictionary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nwse")

    def destroy_dictionary_frame(self):
        self.dictionary_frame.destroy()

    def create_dictionary_frame(self):
        self.destroy_settings_frame()
        self.dictionary_frame = DictionaryFrame(self)
        self.dictionary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nwse")

    def destroy_settings_frame(self):
        self.settings_frame.destroy()

    def create_settings_frame(self):
        self.destroy_dictionary_frame()
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

    def create_history_frame(self):
        self.destroy_dictionary_frame()
        self.settings_frame = HistoryFrame(self)
        self.settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")



class HistoryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.results=[]
        self.grid_columnconfigure(0, weight=1)

        self.hdata = get_history()
        self.position = 1

        self.exit_history_button = customtkinter.CTkButton(self, text= "Exit history", command=self.exit_history_callback, font=("Calibri", 22))
        self.exit_history_button.grid(row=0, column=0, padx=30, pady=(30,15), sticky="nswe")

        for self.entry in self.hdata:
            self.add_result(self.entry[0], self.entry[1], self.position)
            self.position += 1

    def exit_history_callback(self):
        self.destroy()

    def add_result(self, searchterm, time, position): # Add a single result. Has a field for each attribute of the CC-CEDICT dictionary
        SingleResult = SingleHistoryFrame(self, searchterm, time)
        SingleResult.grid(row=position, column=0, padx=10, pady=10, sticky="we")
        self.results.append(SingleResult)

class SingleHistoryFrame(customtkinter.CTkFrame): # A frame for a single result. Many of these populate a single results frame
    def __init__(self, master, searchterm, time):
        super().__init__(master)

        self.searchterm = searchterm
        self.time = datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        self.time = self.time.replace('\n', '')
        self.time = self.time + " UTC"


        self.grid_rowconfigure((0), weight=0)

        self.searchterm_display = customtkinter.CTkLabel(self, text=self.searchterm, font=("Calibri",24), wraplength=170, justify='left', width=170, anchor='w')
        self.searchterm_display.grid(row=0, column=0, padx=(10, 20), pady=(5,0), sticky="w")

        self.time_display = customtkinter.CTkLabel(self, text=self.time, font=("Calibri",16), wraplength=240, justify='left', anchor='w')
        self.time_display.grid(row=1, column=0, padx=10, pady=(0,5), sticky="w")

class SettingsFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0,1), weight=0)

        self.no_search_label = customtkinter.CTkLabel(self, text="Number of search results to display (default is 30):", font=("Calibri",18), justify='left', anchor='w')
        self.no_search_label.grid(row=0, column=0, padx=30, pady=(10,2), sticky="nswe")

        self.no_search_entry = customtkinter.CTkEntry(self, font=("Calibri",18))  
        self.no_search_entry.grid(row=1, column=0, padx=30, pady=2, sticky="nswe")

        self.no_history_label = customtkinter.CTkLabel(self, text="Number of history entries to store (default is 100):", font=("Calibri",18), justify='left', anchor='w')
        self.no_history_label.grid(row=2, column=0, padx=30, pady=(15,2), sticky="nswe")

        self.no_history_entry = customtkinter.CTkEntry(self, font=("Calibri",18))  
        self.no_history_entry.grid(row=3, column=0, padx=30, pady=2, sticky="nswe")

        self.pinyin_type_label = customtkinter.CTkLabel(self, text="Show pinyin tones with accents, or with numbers:", font=("Calibri",18), justify='left', anchor='w')
        self.pinyin_type_label.grid(row=4, column=0, padx=30, pady=(15,2), sticky="nswe")

        self.pinyin_type_optionmenu = customtkinter.CTkOptionMenu(self, values=["","Accented pinyin tones", "Numeric pinyin tones"], font=("Calibri", 18), dropdown_font=("Calibri", 18))
        self.pinyin_type_optionmenu.grid(row=5, column=0, padx=30, pady=2, sticky="nswe")

        self.theme_label = customtkinter.CTkLabel(self, text="Set the default theme to light or dark (requires restart):", font=("Calibri",18), justify='left', anchor='w')
        self.theme_label.grid(row=6, column=0, padx=30, pady=(10,2), sticky="nswe")

        self.theme_optionmenu = customtkinter.CTkOptionMenu(self, values=["","Dark mode", "Light mode"], font=("Calibri", 18), dropdown_font=("Calibri", 18))
        self.theme_optionmenu.grid(row=7, column=0, padx=30, pady=2, sticky="nswe")

        self.character_label = customtkinter.CTkLabel(self, text="Set the default character type (requires restart):", font=("Calibri",18), justify='left', anchor='w')
        self.character_label.grid(row=8, column=0, padx=30, pady=(15,2), sticky="nswe")

        self.character_optionmenu = customtkinter.CTkOptionMenu(self, values=["","Simplified", "Traditional"], font=("Calibri", 18), dropdown_font=("Calibri", 18))
        self.character_optionmenu.grid(row=9, column=0, padx=30, pady=2, sticky="nswe")

        self.save_button = customtkinter.CTkButton(self, text= "Save changes", command=self.save_changes, font=("Calibri", 22))
        self.save_button.grid(row=10, column=0, padx=30, pady=(30,15), sticky="nswe")
    
        self.discard_button = customtkinter.CTkButton(self, text= "Discard changes", command=self.discard_changes, font=("Calibri", 22))
        self.discard_button.grid(row=11, column=0, padx=30, pady=2, sticky="nswe")

    def save_changes(self):
        self.search_results_max = self.no_search_entry.get()
        self.history_entries_max = self.no_history_entry.get()
        self.pinyin_type = self.pinyin_type_optionmenu.get()
        self.theme = self.theme_optionmenu.get()
        self.character_type = self.character_optionmenu.get()

        if (self.search_results_max == "") or (not (self.search_results_max.isdigit())):
            self.search_results_max = get_field_from_config("search_results_max")
        if (self.history_entries_max == "") or (not (self.history_entries_max.isdigit())):
            self.history_entries_max = get_field_from_config("history_entries_max")
        if self.pinyin_type == "":
            self.pinyin_type = get_field_from_config("pinyin_type")
        if self.theme == "":
            self.theme = get_field_from_config("theme")
        if self.character_type == "":
            self.character_type = get_field_from_config("character_type")

        with open('config.ini', 'w') as f:
            write_string = "search_results_max = {0}\nhistory_entries_max = {1}\npinyin_type = {2}\ntheme = {3}\ncharacter_type = {4}".format(self.search_results_max, self.history_entries_max, self.pinyin_type, self.theme, self.character_type)
            f.write(write_string)
        
        app.create_dictionary_frame()

    def discard_changes(self):
        app.create_dictionary_frame()


class DictionaryFrame(customtkinter.CTkFrame): # Contains the Results and SearchBar frame
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.searchbar_frame = SearchbarFrame(self)
        self.searchbar_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nwe")

        self.results_frame = ResultsFrame(self)
        self.results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.current_result_frame = [self.results_frame]

    def refresh_results_frame(self):
        self.destroy_results_frame()
        self.results_frame = ResultsFrame(self)
        self.results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.current_result_frame = [self.results_frame]
    
    def get_results_frame_width(self):
        self.current_result_frame[0].update()
        return self.current_result_frame[0].winfo_width()

    def destroy_results_frame(self):
        self.results_frame.destroy()
        self.current_result_frame = [None]

if get_field_from_config("theme") == "Dark mode":
    customtkinter.set_appearance_mode("dark")
else:
    customtkinter.set_appearance_mode("light")

customtkinter.set_default_color_theme("blue")

app = App()
app.mainloop()