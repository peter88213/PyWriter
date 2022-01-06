"""Provide a facade class for a GUI featuring just message boxes.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import messagebox
import tkinter as tk
from pywriter.ui.ui import Ui


class UiMb(Ui):
    """UI subclass with messagebox."""

    def __init__(self, title):
        """Override the superclass constructor. """
        root = tk.Tk()
        root.withdraw()
        self.title = title

    def ask_yes_no(self, text):
        """Override the superclass method."""
        return messagebox.askyesno(self.title, text)

    def set_info_how(self, message):
        """Override the superclass method."""

        if message.startswith('ERROR'):
            messagebox.showerror(self.title, message)

        else:
            messagebox.showinfo(self.title, message)
