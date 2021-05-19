"""User interface for the converter: Tk facade

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *
from tkinter import messagebox

from pywriter.ui.ui import Ui


class UiTk(Ui):
    """UI subclass implementing a Tkinter facade."""

    def __init__(self, title):
        """Prepare the graphical user interface. """
        Ui.__init__(self, title)

        self.root = Tk()
        self.root.title(title)

        self.appInfo = Label(self.root, text='')
        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=60)
        self.processInfo = Label(self.root, text='')
        self.root.quitButton = Button(text="Quit", command=quit)
        self.root.quitButton.config(height=1, width=10)

        self.appInfo.grid(row=1, column=1, padx=5, pady=5)
        self.successInfo.grid(row=2, column=1, padx=10, pady=10)
        self.processInfo.grid(row=3, column=1, pady=10)
        self.root.quitButton.grid(row=4, column=1, pady=10)

    def ask_yes_no(self, text):
        return messagebox.askyesno('WARNING', text)

    def set_info_what(self, message):
        """What's the converter going to do?"""

        self.infoWhatText = message
        self.appInfo.config(text=message)

    def set_info_how(self, message):
        """How's the converter doing?"""

        self.infoHowText = message
        self.processInfo.config(text=message)

        if message.startswith('SUCCESS'):
            self.successInfo.config(bg='green')

        else:
            self.successInfo.config(bg='red')

    def start(self):
        self.root.mainloop()
