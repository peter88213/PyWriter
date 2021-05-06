"""User interface for the converter: Tk facade

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *

from pywriter.ui.ui_tk import UiTk


class UiTkOpen(UiTk):
    """Add an 'Open' button to UiTk."""

    def show_open_button(self, open_cmd):
        self.root.openButton = Button(text="Open", command=open_cmd)
        self.root.openButton.config(height=1, width=10)
        self.root.openButton.pack(padx=5, pady=5)
