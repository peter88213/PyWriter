#!/usr/bin/env python3
""""Provide a tkinter GUI class with main menu and main window.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import filedialog

from pywriter.yw.yw7_file import Yw7File


class RootTk():
    """A tkinter GUI root class.
    Main menu, title bar, main window, status bar, path bar.
    """

    def __init__(self, title, **kwargs):
        """Initialize the project related instance variables
        and configure the user interface.
        - Create a main menu to be extended by subclasses.
        - Create a title bar for the project title.
        - Open a main window to be used by subclasses.
        - Create a status bar to be used by subclasses.
        - Create a path bar for the project file path.
        """
        self.kwargs = kwargs
        self.ywPrj = None

        self.root = tk.Tk()
        self.root.title(title)
        self.menubar = tk.Menu(self.root)
        self.menuF = tk.Menu(self.menubar, title='my title', tearoff=0)
        self.menubar.add_cascade(label='Project', menu=self.menuF)
        self.menuF.add_command(label='Open Project...', command=lambda: self.open_project(''))
        self.menuF.add_command(label='Close Project', command=lambda: self.close_project())
        self.menuF.add_command(label='Exit', command=self.root.quit)
        self.extend_menu()
        self.root.config(menu=self.menubar)
        self.titleBar = tk.Label(self.root,  text='')
        self.titleBar.pack(expand=False, anchor='w')
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both', padx=4, pady=4)
        self.statusBar = tk.Label(self.root,  text='')
        self.statusBar.pack(expand=False, anchor='w')
        self.pathBar = tk.Label(self.root,  text='')
        self.pathBar.pack(expand=False, anchor='w')

    def extend_menu(self):
        """Create an object that represents the project file.
        This is a template method that can be overridden by subclasses. 
        """

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self.menuF.entryconfig('Close Project', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self.menuF.entryconfig('Close Project', state='normal')

    def start(self):
        """Start the Tk main loop."""
        self.root.mainloop()

    def instantiate_project(self, fileName):
        """Create an object that represents the project file.
        This is a template method that can be overridden by subclasses. 
        """
        self.ywPrj = Yw7File(fileName)

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Return True if sucessful, otherwise return False.
        """
        initDir = os.path.dirname(fileName)

        if not initDir:
            initDir = './'

        if not fileName:
            fileName = filedialog.askopenfilename(filetypes=[('yWriter 7 project', '.yw7')],
                                                  defaultextension='.yw7', initialdir=initDir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.pathBar.config(text=os.path.normpath(fileName))
            self.instantiate_project(fileName)
            message = self.ywPrj.read()

            if not message.startswith('ERROR'):

                if self.ywPrj.title:
                    titleView = self.ywPrj.title

                else:
                    titleView = 'Untitled yWriter project'

                if self.ywPrj.author:
                    authorView = self.ywPrj.author

                else:
                    authorView = 'Unknown author'

                self.titleBar.config(text=titleView + ' by ' + authorView)
                self.enable_menu()
                return True

            else:
                self.close_project()
                self.statusBar.config(text=message)

        return False

    def close_project(self):
        """Close the yWriter project without saving.
        Reset the user interface.
        """
        self.ywPrj = None
        self.titleBar.config(text='')
        self.statusBar.config(text='')
        self.pathBar.config(text='')
        self.disable_menu()
