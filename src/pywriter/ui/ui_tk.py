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

        self._root = Tk()
        self._root.minsize(400, 150)
        self._root.resizable(width=FALSE, height=FALSE)
        self._root.title(title)

        self._appInfo = Label(self._root, text='')
        self._appInfo.pack(padx=20, pady=5)

        self._processInfo = Label(self._root, text='', padx=20)
        self._processInfo.pack(pady=20, fill='both')

        self._root.quitButton = Button(text="Quit", command=quit)
        self._root.quitButton.config(height=1, width=10)
        self._root.quitButton.pack(pady=10)

    def ask_yes_no(self, text):
        """Override the Ui method."""
        return messagebox.askyesno('WARNING', text)

    def set_info_what(self, message):
        """What's the converter going to do?"""
        self.infoWhatText = message
        self._appInfo.config(text=message)

    def set_info_how(self, message):
        """How's the converter doing?"""

        if message.startswith(ERROR):
            self._processInfo.config(bg='red')
            self._processInfo.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()

        else:
            self._processInfo.config(bg='green')
            self._processInfo.config(fg='white')
            self.infoHowText = message

        self._processInfo.config(text=self.infoHowText)

    def start(self):
        """Start the Tk main loop."""
        self._root.mainloop()

    def show_open_button(self, open_cmd):
        """Add an 'Open' button to the main window."""
        self._root.openButton = Button(text="Open", command=open_cmd)
        self._root.openButton.config(height=1, width=10)
        self._root.openButton.pack(pady=10)
