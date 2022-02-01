#!/usr/bin/env python3
""""Provide a tkinter GUI class with main menu and main window.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class MainTk(Ui):
    """A tkinter GUI root class.
    Main menu, title bar, main window frame, status bar, path bar.
    """

    def __init__(self, title, **kwargs):
        """Initialize the project related instance variables
        and configure the user interface.
        - Create a main menu to be extended by subclasses.
        - Create a title bar for the project title.
        - Open a main window frame to be used by subclasses.
        - Create a status bar to be used by subclasses.
        - Create a path bar for the project file path.
        """
        super().__init__(title)
        self.statusText = ''
        self.kwargs = kwargs
        self.ywPrj = None

        self.root = tk.Tk()
        self.root.title(title)
        self.mainMenu = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open...', command=lambda: self.open_project(''))
        self.fileMenu.add_command(label='Close', command=lambda: self.close_project())
        self.fileMenu.entryconfig('Close', state='disabled')
        self.fileMenu.add_command(label='Exit', command=self.root.quit)
        self.extend_menu()
        # Hook for subclasses
        self.root.config(menu=self.mainMenu)
        self.titleBar = tk.Label(self.root, text='', padx=5, pady=2)
        self.titleBar.pack(expand=False, anchor='w')
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both')
        self.statusBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=2)
        self.statusBar.pack(expand=False, fill='both')
        self.pathBar = tk.Label(self.root, text='', padx=5, pady=3)
        self.pathBar.pack(expand=False, anchor='w')

    def extend_menu(self):
        """Create an object that represents the project file.
        This is a template method that can be overridden by subclasses. 
        """

    def disable_menu(self):
        """Disable menu entries when no project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close', state='normal')

    def start(self):
        """Start the user interface.
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def open_project(self, fileName, fileTypes=[('yWriter 7 project', '.yw7')]):
        """Select a valid project file and display the path.

        Priority:
        1. use file name argument
        2. open file select dialog

        Return the file name.
        To be extended by subclasses.
        """
        self.set_status(self.statusText)
        initDir = os.path.dirname(self.kwargs['yw_last_open'])

        if not initDir:
            initDir = './'

        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(filetypes=fileTypes, defaultextension='.yw7', initialdir=initDir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.pathBar.config(text=os.path.normpath(fileName))

        return fileName

    def close_project(self):
        """Close the yWriter project without saving.
        Reset the user interface.
        To be extended by subclasses.
        """
        self.ywPrj = None
        self.titleBar.config(text='')
        self.set_status('')
        self.pathBar.config(text='')
        self.disable_menu()

    def ask_yes_no(self, text):
        """Display a message box with "yes/no" options.
        Return True or False depending on user input.
        """
        return messagebox.askyesno('WARNING', text)

    def set_info_how(self, message):
        """How's the application doing?
        Put a message on the status bar.
        """

        if message.startswith(ERROR):
            self.statusBar.config(bg='red')
            self.statusBar.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()

        else:
            self.statusBar.config(bg='green')
            self.statusBar.config(fg='white')
            self.infoHowText = message

        self.statusBar.config(text=self.infoHowText)

    def set_status(self, message):
        """Put text on the status bar."""
        self.statusText = message
        self.statusBar.config(bg=self.root.cget('background'))
        self.statusBar.config(fg='black')
        self.statusBar.config(text=message)
