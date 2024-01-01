from PIL import ImageTk,Image
import pandas as pd
import numpy as np
import json

class Data():
    def __del__(self):
        json.data = {
            'native_lang' : self.native_lang,
            'active_language' : self.active_language
        }
        self.prase_data['native_lang'] = self.native_lang
        self.prase_data[f'active_language_{self.native_lang}'] = self.active_language
        self.settings_file.write(json.dumps(self.prase_data,indent=4))

    def __init__(self):
        self.supported_languages = ['en','fr','de','es','ja','it','he']
        self.subjects = ['Top 100','Top 400','Top 1000','Animals','Food']

        self.font = 'David'
        self.font_2 = 'FuturistStencil'
        self.colors = {
            'main' : '#b469ff',
            'white' : '#FAF9F6'
        }

        self.word_list = None
        self.progress_list = None

        self.logos = {}
        self.dictionary = {}
        self.borders = {}
        self.generals = {}

        self.settings_file = open('resources/pylang/settings.json',mode='r')
        self.prase_data = json.load(self.settings_file)
        self.native_lang = self.prase_data['native_lang']
        self.active_language = self.prase_data[f'active_language_{self.native_lang}']
        self.settings_file = open('resources/pylang/settings.json', mode='w')

        self.load_images()
    def load_images(self):
        for lang in self.supported_languages:
            self.logos[lang] = ImageTk.PhotoImage(file=f'resources/pylang/images/{lang}.png')
        self.logos['main'] = ImageTk.PhotoImage(Image.open(fp='resources/pylang/images/main_logo.png'))
        self.logos['main_small'] = ImageTk.PhotoImage(Image.open(fp='resources/pylang/images/main_logo.png').resize(size=(140,35)))


        self.borders['border'] = ImageTk.PhotoImage(file='resources/pylang/images/border.png')
        self.borders['big_up'] = ImageTk.PhotoImage(file='resources/pylang/images/big_border_upside.png')
        self.borders['big_down'] = ImageTk.PhotoImage(file='resources/pylang/images/big_border_downside.png')
        self.borders['selected'] = ImageTk.PhotoImage(file='resources/pylang/images/selected_border.png')
        self.borders['non'] =ImageTk.PhotoImage(file='resources/pylang/images/non_selected_border.png')
        self.borders['shade'] = ImageTk.PhotoImage(file='resources/pylang/images/border_shade.png')
        self.borders['loadbar'] = ImageTk.PhotoImage(file='resources/pylang/images/loadbar_border.png')

        self.generals['return'] = ImageTk.PhotoImage(file='resources/pylang/images/return.png')
        self.generals['start'] = ImageTk.PhotoImage(Image.open(fp='resources/pylang/images/start.png').resize(size=(60,60)))
        self.generals['start_s'] = ImageTk.PhotoImage(Image.open(fp='resources/pylang/images/start.png').resize(size=(49,40)))
        self.generals['loadbar'] = Image.open(fp='resources/pylang/images/loadbar.png')
        self.generals['check_button'] = ImageTk.PhotoImage(file='resources/pylang/images/check_button.png')
        self.generals['cancel_button'] = ImageTk.PhotoImage(file='resources/pylang/images/cancel_button.png')

    def load_menu(self,lang):
        temp_csv = pd.read_csv('resources/pylang/menu.csv')
        return temp_csv[lang]

    def load_language(self,lang):
        temp_csv = pd.read_csv('resources/pylang/languages.csv')
        return temp_csv[lang]

    def get_loadbar(self,percentage):
        temp_loadbar = self.generals['loadbar'].crop((0,0,155*(percentage/100),15))
        temp_loadbar = ImageTk.PhotoImage(temp_loadbar)
        return temp_loadbar

    def get_lists(self,subject,lang):
        self.word_list = pd.read_csv(f'resources/pylang/words/{subject}.csv').copy()
        self.progress_list = pd.read_csv(f'resources/pylang/progress/{subject}_{self.native_lang}_progress.csv').copy()

        for n,word in enumerate(self.progress_list[lang]):
            self.word_list[self.word_list[lang] == word] = np.nan

    def update_progress(self,subject,learned_lang,word):
        word_list = self.progress_list[learned_lang].dropna()

        self.progress_list.loc[len(word_list),learned_lang] = word
        self.progress_list.to_csv(path_or_buf=f'resources/pylang/progress/{subject}_{self.native_lang}_progress.csv',index=False)

        self.word_list[self.word_list[learned_lang] == word] = np.nan


