"""User interface for the converter: Tk facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *
from tkinter import messagebox

TITLE = 'yWriter import/export'


class CnvUiTk():

    def __init__(self):
        """initialize GUI. """

        # Prepare the graphical user interface.

        self.root = Tk()
        self.root.geometry("800x360")
        self.root.title(TITLE)
        self.header = Label(self.root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(self.root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.successInfo = Label(self.root)
        self.successInfo.pack(fill=X, expand=1, padx=50, pady=5)
        self.processInfo = Label(self.root, text='')
        self.processInfo.pack(padx=5, pady=5)

        self.processInfoText = ''

    def ask_yes_no(self, text):
        return messagebox.askyesno('WARNING', text)

    def set_app_info(self, message):
        self.appInfo.config(text=message)

    def set_process_info(self, message):
        self.processInfoText = message
        self.processInfo.config(text=message)

    def get_process_info(self):
        return self.processInfoText

    def show_success(self, success):

        if success:
            self.successInfo.config(bg='green')

        else:
            self.successInfo.config(bg='red')

        self.root.quitButton = Button(text="Quit", command=quit)
        self.root.quitButton.config(height=1, width=10)
        self.root.quitButton.pack(padx=5, pady=5)
        self.root.mainloop()
