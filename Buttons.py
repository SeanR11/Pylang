from tkinter import Button

class Button(Button):
    def __init__(self,master, command=None):
        super().__init__(master=master)
        self['borderwidth'] = 0
        self['bg'] = self.master['bg']
        self['command'] = command
        self['activebackground'] = self.master['bg']

class LanguageSettingsButton(Button):
    def __init__(self,master, image, command):
        super().__init__(master=master,command=command)
        self['image'] = image

class MenuButton(Button):
    def __init__(self,master, text, command,font):
        super().__init__(master=master,command=command)
        self['text'] = text
        self['font'] = (font,25)
        self['fg'] = '#040814'


