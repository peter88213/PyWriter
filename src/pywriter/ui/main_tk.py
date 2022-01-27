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


class MainTk():
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
        self.kwargs = kwargs
        self.ywPrj = None

        self.root = tk.Tk()
        self.root.title(title)
        self.mainMenu = tk.Menu(self.root)
        self.fileMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Project...', command=lambda: self.open_project(''))
        self.fileMenu.add_command(label='Close Project', command=lambda: self.close_project())
        self.fileMenu.entryconfig('Close Project', state='disabled')
        self.fileMenu.add_command(label='Exit', command=self.root.quit)
        self.extend_menu()
        # Hook for subclasses
        self.root.config(menu=self.mainMenu)
        self.titleBar = tk.Label(self.root,  text='')
        self.titleBar.pack(expand=False, anchor='w')
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both')
        self.statusBar = tk.Label(self.root,  text='')
        self.statusBar.pack(expand=False, anchor='w')
        self.pathBar = tk.Label(self.root,  text='')
        self.pathBar.pack(expand=False, anchor='w')

    def extend_menu(self):
        """Create an object that represents the project file.
        This is a template method that can be overridden by subclasses. 
        """

    def disable_menu(self):
        """Disable menu entries when no project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close Project', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig('Close Project', state='normal')

    def start(self):
        """Start the user interface.
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def open_project(self, fileName):
        """Select a valid project file and display the path.

        Priority:
        1. use file name argument
        2. open file select dialog

        Return the file name.
        To be extended by subclasses.
        """
        initDir = os.path.dirname(self.kwargs['yw_last_open'])

        if not initDir:
            initDir = './'

        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(filetypes=[('yWriter 7 project', '.yw7')],
                                                  defaultextension='.yw7', initialdir=initDir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.pathBar.config(text=os.path.normpath(fileName))

        self.statusBar.config(text='')
        return fileName

    def close_project(self):
        """Close the yWriter project without saving.
        Reset the user interface.
        To be extended by subclasses.
        """
        self.ywPrj = None
        self.titleBar.config(text='')
        self.statusBar.config(text='')
        self.pathBar.config(text='')
        self.disable_menu()

    def ask_yes_no(self, text):
        """Display a message box with "yes/no" options.
        Return True or False depending on user input.
        """
        return messagebox.askyesno('WARNING', text)
