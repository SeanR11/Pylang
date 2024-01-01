import pandas as pd
from tkinter import Tk,Frame,Canvas
from Data import Data
from Buttons import LanguageSettingsButton,MenuButton
from NewLearnFrame import NewLearnFrame
from ContinueLearnFrame import ContinueLearnFrame

MAIN_COLOR = '#b469ff'
MAIN_COLOR_LIGHT = '#cd9cff'
SECOND_COLOR = '#040814'
SECOND_COLOR_LIGHT = '#0c193e'
OFF_WHITE = '#FAF9F6'

class MainWindow(Tk):
    def __init__(self, title, width, height):
        #window settings
        super().__init__()
        self.title(title)
        self.geometry('1x1+600+200')
        self.minsize(width=width, height=height)
        self.width = width
        self.height = height
        self['bg'] = MAIN_COLOR

        #general settings
        self.data = Data()

        #settings_frame
        self.settings_container = Frame(master=self,bg=self['bg'],borderwidth=0)
        self.settings_container.place(x=self.width*0.94, y=self.height*0.01)

        self.language_button = LanguageSettingsButton(master=self.settings_container,
                                                      image=self.data.logos[self.data.native_lang],
                                                      command=self.open_lang_menu)
        self.language_button.grid(column=0,row=0)


        #menu_frame
        self.menu = self.data.load_menu(self.data.native_lang)
        item_spaces = 25

        self.menu_container = Frame(master=self,bg=OFF_WHITE)
        self.menu_container.place(x=self.width/2, y=self.height/2,anchor='center')

        self.logo = Canvas(self.menu_container,width=240,height=60,highlightthickness=0,bg=self.menu_container['bg'])
        self.logo.create_image(0,0,image = self.data.logos['main'],anchor='nw')
        self.logo.pack(pady=item_spaces/2,anchor='center')

        self.learn_new_button = MenuButton(self.menu_container,text=self.menu[0],font=self.data.font,
                                           command=lambda : NewLearnFrame(self,self.data))
        self.learn_new_button.pack(pady=item_spaces)

        self.continue_learn_button = MenuButton(self.menu_container, text=self.menu[1],font=self.data.font,
                                                command=lambda: ContinueLearnFrame(master=self,data=self.data))
        self.continue_learn_button.pack(pady=item_spaces)

        self.exit_button = MenuButton(self.menu_container,font=self.data.font,text=self.menu[2],command=self.destroy)
        self.exit_button.pack(pady=item_spaces)


    def open_lang_menu(self):
        if len(self.settings_container.children) <= 1:
            row_parm = 0
            for language in self.data.supported_languages:
                if language != self.data.native_lang:
                    row_parm += 1
                    LanguageSettingsButton(master=self.settings_container, image=self.data.logos[language],
                                           command=lambda lang=language: self.update_language(lang)).grid(column=0,row=row_parm)
        else:
            self.close_lang_menu()

    def update_language(self,lang):
        self.data.native_lang = lang
        self.language_button.config(image=self.data.logos[lang])
        self.menu = self.data.load_menu(self.data.native_lang)
        self.learn_new_button['text'] = self.menu[0]
        self.continue_learn_button['text'] = self.menu[1]
        self.exit_button['text'] = self.menu[2]
        self.close_lang_menu()
        self.data.active_language = self.data.prase_data[f'active_language_{self.data.native_lang}']

        for subject in self.data.subjects:
            try:
                open(f'resources/pylang/progress/{subject}_{self.data.native_lang}_progress.csv')
            except:
                df = pd.DataFrame(columns=self.data.supported_languages)
                df.to_csv(f'resources/pylang/progress/{subject}_{self.data.native_lang}_progress.csv')

    def close_lang_menu(self):
        for child in self.settings_container.winfo_children()[1:]:
            child.destroy()

if __name__ == '__main__':

    MainWindow = MainWindow('Pylang',800,600)

    MainWindow.mainloop()