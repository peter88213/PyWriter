"""Provide a facade class for a Tkinter based GUI.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *
from tkinter import messagebox

from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class UiTk(Ui):
    """UI subclass implementing a Tkinter facade."""

    def __init__(self, title):
        """Extend the Ui constructor. """
        super().__init__(title)

        self.root = Tk()
        self.root.minsize(400, 150)
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.title(title)

        self.rowCount = 1
        self.appInfo = Label(self.root, text='')
        self.appInfo.pack(padx=20, pady=5)

        self.rowCount += 1
        self.processInfo = Label(self.root, text='', padx=20)
        self.processInfo.pack(pady=20, fill='both')

        self.rowCount += 1
        self.root.quitButton = Button(text="Quit", command=quit)
        self.root.quitButton.config(height=1, width=10)
        self.root.quitButton.pack(pady=10)

    def ask_yes_no(self, text):
        """Override the Ui method."""
        return messagebox.askyesno('WARNING', text)

    def set_info_what(self, message):
        """What's the converter going to do?"""

        self.infoWhatText = message
        self.appInfo.config(text=message)

    def set_info_how(self, message):
        """How's the converter doing?"""

        if message.startswith(ERROR):
            self.processInfo.config(bg='red')
            self.processInfo.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()

        else:
            self.processInfo.config(bg='green')
            self.processInfo.config(fg='white')
            self.infoHowText = message

        self.processInfo.config(text=self.infoHowText)

    def start(self):
        """Start the Tk main loop."""
        self.root.mainloop()

    def show_open_button(self, open_cmd):
        """Add an 'Open' button to the main window."""
        self.root.openButton = Button(text="Open", command=open_cmd)
        self.root.openButton.config(height=1, width=10)
        self.rowCount += 1
        self.root.openButton.pack(pady=10)
