"""Provide a facade for a Tkinter GUI with an additional 'Open' button.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *

from pywriter.ui.ui_tk import UiTk


class UiTkOpen(UiTk):
    """Extend the UiTk class with an additional 'Open' button."""

    def show_open_button(self, open_cmd):
        """Add an 'Open' button to UiTk."""
        self.root.openButton = Button(text="Open", command=open_cmd)
        self.root.openButton.config(height=1, width=10)
        self.rowCount += 1
        self.root.openButton.grid(row=self.rowCount, column=1, pady=10)
