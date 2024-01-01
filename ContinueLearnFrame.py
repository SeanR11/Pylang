import random
import numpy as np
from SubFrame import SubFrame
from Buttons import LanguageSettingsButton
from tkinter import Canvas

class ContinueLearnFrame(SubFrame):
    def __init__(self,master,data,selected_lang=None):
        super().__init__(master=master, data=data, headline='Choose Language')

        self.main_frame.grid_propagate(False)
        self.main_frame.pack_propagate(False)

        self.cards = []
        self.cards_loadbar = []
        self.buttons = []
        self.words = {}
        self.selected_lang = selected_lang

        if self.selected_lang == None:
            self.load_languages()

    def learn_language(self,lang):
        self.selected_lang = lang
        self.load_subjects()

    def erase(self):
        for card in self.cards:
            card.destroy()
        for button in self.buttons:
            button.destroy()

        self.cards = []
        self.buttons = []
        self.cards_loadbar = []

    def load_languages(self):
        self.erase()

        self.header.config(text="Choose Language")
        self.return_button.config(command=self.destroy)

        for col in range(0, 3):
            self.main_frame.columnconfigure(index=col, pad=25)
        for row in range(0, int(len(self.data.active_language) / 3) + 1):
            self.main_frame.rowconfigure(index=row, pad=25)

        col = 0
        row = 0
        for index, lang in enumerate(self.data.active_language):
            card = Canvas(master=self.main_frame, width=240, height=160, bg=self.main_frame['bg'], highlightthickness=0)
            card.create_image(120, 80, image=self.data.borders['border'], tag='border')
            card.create_text(120, 50, text=self.data.active_language[index], font=(self.data.font, 25))
            card.create_image(120, 110, image=self.data.logos[lang])
            card.grid(column=col, row=row)
            card.bind("<Button-1>", lambda e, l=lang: self.learn_language(l))
            if col < 2:
                col += 1
            else:
                row += 1
                col = 0
            self.cards.append(card)

    def load_subjects(self):

        self.erase()

        self.header.config(text="Choose Subject")
        self.return_button.config(command=self.load_languages)


        for col in range(0, 3):
            self.main_frame.columnconfigure(index=col, pad=25)
        for row in range(0, int(len(self.data.subjects) / 3) + 1):
            self.main_frame.rowconfigure(index=row, pad=25)
        col = 0
        row = 0
        for index, subj in enumerate(self.data.subjects):
            self.data.get_lists(subject=subj,lang=self.selected_lang)

            total = len(self.data.word_list[self.selected_lang])
            progress = len(self.data.progress_list[self.selected_lang].dropna())
            precent = round((progress/total)*100)

            self.cards_loadbar.append(self.data.get_loadbar(precent))
            card = Canvas(master=self.main_frame, width=240, height=160, bg=self.main_frame['bg'], highlightthickness=0)
            if len(self.data.word_list[self.selected_lang].dropna()) != 0:
                card.create_image(120, 80, image=self.data.borders['loadbar'], tag='border')
                card.create_image(14, 135, image=self.cards_loadbar[-1], tag='loadbar',anchor='w')
                card.create_text(205, 135, text=f'{precent}%', font=(self.data.font, 16))
                card.create_text(120, 90, text=f'{progress}/'
                                               f'{total}',
                                 font=(self.data.font, 25))
                card.bind("<Button-1>", lambda e, sub=self.data.subjects[index]: self.load_learn_program(sub))
            else:
                card.create_image(120, 80, image=self.data.borders['border'], tag='border')
                card.create_text(120, 135, text=f'COMPLETED', font=(self.data.font, 16))
                card.create_text(120, 90, text='100%',
                                 font=(self.data.font, 25))

            card.create_text(120, 40, text=self.data.subjects[index], font=(self.data.font, 30))

            card.grid(column=col, row=row)

            if col < 2:
                col += 1
            else:
                row += 1
                col = 0
            self.cards.append(card)

    def load_learn_program(self,subject):
        self.data.get_lists(subject=subject,lang=self.selected_lang)

        def load_cards(self):
            card_upside = Canvas(master=self.main_frame, width=600, height=400, bg=self.main_frame['bg'],
                                 highlightthickness=0)
            card_upside.create_image(300, 200, image=self.data.borders['big_up'], tag='border')
            card_upside.create_text(300, 100,
                                    text=f'{self.data.load_language(lang=self.data.native_lang)[self.data.supported_languages.index(self.selected_lang)]}',
                                    font=(self.data.font, 50),
                                    tags='headline')
            card_upside.create_text(300,250,text='',font=(self.data.font, 30),tags='word')
            card_upside.bind("<Button-1>", lambda e: swap_cards(self, 0))
            card_upside.pack(pady=40)
            self.cards.append(card_upside)


            card_downside = Canvas(master=self.main_frame, width=600, height=400, bg=self.main_frame['bg'],
                                   highlightthickness=0)
            card_downside.create_image(300, 200, image=self.data.borders['big_down'], tag='border')
            card_downside.create_text(300, 100,
                                    text=f'{self.data.load_language(lang=self.data.native_lang)[self.data.supported_languages.index(self.data.native_lang)]}',
                                    font=(self.data.font, 50),
                                    tags='headline')
            card_downside.create_text(300,250,text='',font=(self.data.font, 30),tags='word')
            card_downside.bind("<Button-1>", lambda e: swap_cards(self, 1))
            self.cards.append(card_downside)

        def swap_cards(self, index):
            if index == 0:
                self.cards[0].pack_forget()
                self.cards[1].pack(pady=40)
            else:
                self.cards[0].pack(pady=40)
                self.cards[1].pack_forget()

        def update_cards(self):
            while(True):
                try:
                    random_word = random.choice(self.data.word_list[self.selected_lang].dropna().tolist())
                    if random_word != np.nan and random_word != np.NaN:
                        current_word_index = self.data.word_list.index[self.data.word_list[self.selected_lang] == random_word].tolist()[0]
                        self.words['native'] = self.data.word_list[self.data.native_lang][current_word_index]
                        self.words['learned'] = self.data.word_list[self.selected_lang][current_word_index]
                        self.cards[0].itemconfigure('word', text=f'{self.words['learned']}')
                        self.cards[1].itemconfigure('word', text=f'{self.words['native']}')
                        break
                except IndexError as e:
                    self.cards[0].itemconfigure(tagOrId='headline',text='Congratulations')
                    self.cards[0].itemconfigure(tagOrId='word',text='Subject completed')
                    for button in self.buttons:
                        button.destroy()
                    break

            try:
                self.cards[0].pack_info()
            except:
                swap_cards(self,1)

        def approval_word(self):
            self.data.update_progress(subject=subject,learned_lang=self.selected_lang,word=self.words['learned'])
            update_cards(self)

        self.erase()

        self.header.config(text=f"{subject}")
        self.return_button.config(command=self.load_subjects)


        load_cards(self)
        update_cards(self)


        check_button = LanguageSettingsButton(master=self.main_frame, image=self.data.generals['check_button'],
                                               command=lambda : approval_word(self))
        check_button.place(x=300, y=500, anchor='center')
        self.buttons.append(check_button)

        cancel_button = LanguageSettingsButton(master=self.main_frame, image=self.data.generals['cancel_button'],
                                               command=lambda : update_cards(self))
        cancel_button.place(x=500,y=500,anchor='center')
        self.buttons.append(cancel_button)


