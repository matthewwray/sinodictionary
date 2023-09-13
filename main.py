import customtkinter
from PIL import Image, ImageTk
from search_alg import search_alg
from pinyin_converter import numeric_to_accent
from split_pinyin import split_pinyin
from pinyin_list_generators import fix_ncolon

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

def remove_non_alphanumeric(string):
    new_string = ""
    valid_chars= [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    for char in string:
        if char in valid_chars:
            new_string += char
    return new_string
    
class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.simple_characters = True

        self.appearance_mode = "dark"

        self.moon_graphic = customtkinter.CTkImage(Image.open("graphic/moon-90.png"))
        self.sun_graphic = customtkinter.CTkImage(Image.open("graphic/sun-100.png"))
        #self.settings_graphic = customtkinter.CTkImage(Image.open("graphic/setting-100.png"))
        self.traditional_graphic = customtkinter.CTkImage(Image.open("graphic/traditional.png"))
        self.simplified_graphic = customtkinter.CTkImage(Image.open("graphic/simplified.png"))
        #self.history_graphic = customtkinter.CTkImage(Image.open("graphic/history-100.png"))
        #self.camera_graphic = customtkinter.CTkImage(Image.open("graphic/camera-100.png"))

        #self.settings_button = customtkinter.CTkButton(self, image=self.settings_graphic, text="", command=self.nothing, width=64, height=64)
        #self.settings_button.grid(row=0, column=0, padx=15, pady=10, sticky="ewns")

        self.appearance_mode_button = customtkinter.CTkButton(self, image=self.moon_graphic, text="", command=self.appearance_mode_button_callback, width=64, height=64)
        self.appearance_mode_button.grid(row=1, column=0, padx=15, pady=(15,10), sticky="ewns")

        self.simplified_characters_button = customtkinter.CTkButton(self, image=self.simplified_graphic, text="", command=self.simple_characters_button_callback, width=64, height=64)
        self.simplified_characters_button.grid(row=2, column=0, padx=15, pady=10, sticky="ewns")

        #self.history_button = customtkinter.CTkButton(self, image=self.history_graphic, text="", command=self.nothing, width=64, height=64)
        #self.history_button.grid(row=3, column=0, padx=15, pady=10, sticky="ewns")

        #self.camera_button = customtkinter.CTkButton(self, image=self.camera_graphic, text="", command=self.nothing, width=64, height=64)
        #self.camera_button.grid(row=4, column=0, padx=15, pady=10, sticky="ewns")
    
    def nothing(self):
        pass

    def simple_characters_button_callback(self):
        if self.simple_characters == True:
            self.simple_characters = False
            self.simplified_characters_button.configure(image=self.traditional_graphic)
        
        else:
            self.simple_characters = True
            self.simplified_characters_button.configure(image=self.simplified_graphic)

    def appearance_mode_button_callback(self):
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"
            self.appearance_mode_button.configure(image=self.sun_graphic)
        else:
            self.appearance_mode = "dark"
            self.appearance_mode_button.configure(image=self.moon_graphic)
        customtkinter.set_appearance_mode(self.appearance_mode)

class SearchbarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.MAX_RESULTS = 30
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

    def toggle_language(self):
        if self.current_language == 'CHINESE':
            self.set_language('ENGLISH')
        else:
            self.set_language('CHINESE')
    
    def set_language(self, lang):
        if lang == 'CHINESE':
            self.current_language = lang
            self.language_toggle_button.configure(image=self.language_toggle_chinese_graphic)
        elif lang == 'ENGLISH':
            self.current_language = lang
            self.language_toggle_button.configure(image=self.language_toggle_english_graphic)

    def get_search(self):
        app.dictionary_frame.results_frame.clear_results()
        app.dictionary_frame.refresh_results_frame()

        search = self.textbox.get()
        search_results, returned_search_lang = search_alg(search, self.current_language)
        search_results = search_results[0:self.MAX_RESULTS]
        
        self.set_language(returned_search_lang)

        if app.sidebar_frame.simple_characters == True:
            writing_system = 'simplified'
        else:
            writing_system = 'traditional'
        for result in search_results:
            app.dictionary_frame.results_frame.add_result(result[writing_system], result['pinyin'], result['english'])

    def pressed_enter(self, event):
        self.get_search()
    
    def search_button_callback(self):
        self.get_search()

class ResultsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.results=[]
        self.grid_columnconfigure(0, weight=1)

    def add_result(self, chinese, pinyin, english):
        SingleResult = SingleResultFrame(self, chinese, pinyin, english)
        SingleResult.grid(row=len(self.results), column=0, padx=10, pady=10, sticky="we")
        self.results.append(SingleResult)

    def clear_results(self):
        for result in self.results:
            result.destroy()
        self.results = []

class SingleResultFrame(customtkinter.CTkFrame):
    def __init__(self, master, chinese, pinyin, english):
        super().__init__(master)

        self.chinese = chinese
        self.pinyin = pinyin.lower()
        self.english = english

        self.pinyin = fix_ncolon(self.pinyin)
        self.pinyin = remove_non_alphanumeric(self.pinyin)
        
        self.pinyin.replace("'",'')
        self.pinyin = ''.join(numeric_to_accent(split_pinyin(self.pinyin)))

        self.grid_rowconfigure((0), weight=0)

        self.chinese_display = customtkinter.CTkLabel(self, text=self.chinese, font=("Calibri",24), wraplength=170, justify='left', width=170, anchor='w') # 是
        self.chinese_display.grid(row=0, column=0, padx=(10, 20), pady=(5,0), sticky="w")

        self.pinyin_display = customtkinter.CTkLabel(self, text=self.pinyin, font=("Calibri",16), wraplength=170, justify='left', anchor='w')
        self.pinyin_display.grid(row=1, column=0, padx=10, pady=(0,5), sticky="w")

        self.english_display = customtkinter.CTkLabel(self, text=self.english, font=("Calibri",16), wraplength= app.dictionary_frame.get_results_frame_width()-240, justify='left', anchor='w')
        self.english_display.grid(row=0, column=1, padx=10, pady=5, sticky="w", rowspan=2)

class App(customtkinter.CTk):
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

        #self.create_settings_frame()

    def destroy_dictionary_frame(self):
        self.dictionary_frame.destroy()

    def create_settings_frame(self):
        self.destroy_dictionary_frame()
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

class DictionaryFrame(customtkinter.CTkFrame):
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

app = App()
app.mainloop()