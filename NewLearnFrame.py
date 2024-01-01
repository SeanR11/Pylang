from tkinter import Canvas
from Buttons import LanguageSettingsButton
from SubFrame import SubFrame

class NewLearnFrame(SubFrame):
    def __init__(self,master,data):
        super().__init__(master=master, data=data, headline='Choose Language')

        self.lang_cards = []
        self.selected_card = None
        self.language_list = self.data.load_language(self.data.native_lang)

        self.main_frame.grid_propagate(False)
        for x in range(0,int(len(self.data.supported_languages)/3)+1):
            if x < 3:
                self.main_frame.columnconfigure(index=x,pad=25)
            self.main_frame.rowconfigure(index=x,pad=25)

        row = 0
        col = 0
        for index,lang in enumerate(self.data.supported_languages):
            card = Canvas(master=self.main_frame, width=240, height=160,bg=self.main_frame['bg'],highlightthickness=0)
            card.create_image(120, 80, image=self.data.borders['non'],tag='border')
            card.create_text(120,30,text=self.language_list[index],font=(self.data.font,25))
            card.create_image(120, 80, image=self.data.logos[lang])
            if lang == self.data.native_lang or lang in self.data.active_language:
                card.create_image(120,80,image=self.data.borders['shade'],tag='shade')

            card.grid(column=col,row=row)
            card.bind("<Button-1>",lambda e,i=index:self.select_card(i))
            col += 1
            if col == 3:
                col = 0
                row += 1
            self.lang_cards.append(card)

        self.start_learn_button = LanguageSettingsButton(master=self.main_frame,image=self.data.generals['start'],
                                                         command=lambda : self.add_language(self.selected_card))
        self.start_learn_button.grid(column=2,row=row,sticky='se',pady=10)

    def add_language(self,language):
        self.data.active_language.append(self.data.supported_languages[self.lang_cards.index(language)])
        self.destroy()

    def select_card(self,index):
        if self.data.native_lang != self.data.supported_languages[index] and self.data.supported_languages[index] not in self.data.active_language:
            if self.selected_card == None:

                self.selected_card = self.lang_cards[index]
                self.selected_card.itemconfig('border',image=self.data.borders['selected'])
                return

            self.selected_card.itemconfig('border',image=self.data.borders['non'])
            self.selected_card = self.lang_cards[index]
            self.selected_card.itemconfig('border', image=self.data.borders['selected'])
