from tkinter import Frame,Canvas,Label
from Buttons import *

class SubFrame(Frame):
    def __init__(self,master,data,headline):
        super().__init__(master=master,width=master.width,height=master.height,bg=master['bg'])
        self.width = master.width
        self.height = master.height
        self.pack_propagate(False)
        self.pack()

        self.data = data

        self.header_frame = Frame(master=self,width=self.width,height=self.height*0.08,
                                  bg=self.data.colors['white'])
        self.header_frame.pack_propagate(False)
        self.header_frame.pack()

        self.return_button = LanguageSettingsButton(master=self.header_frame, image=self.data.generals['return'],
                                                    command=self.destroy)
        self.return_button.pack(side='left', pady=5, padx=10)

        self.logo = Canvas(master=self.header_frame, width=140, height=35, highlightthickness=0,
                           bg=self.header_frame['bg'])
        self.logo.create_image(70, 35 / 2, image=self.data.logos['main_small'])
        self.logo.pack(side='right', pady=5, padx=10)

        self.header = Label(master=self.header_frame, text=headline, font=(self.data.font, 20),
                            bg=self.header_frame['bg'])
        self.header.pack(pady=5)

        self.main_frame = Frame(master=self, width=self.width, height=self.height - 50, bg=self['bg'])
        self.main_frame.pack()

    def clear_frames(self):
        self.main_frame.destroy()
        self.header_frame.destroy()

