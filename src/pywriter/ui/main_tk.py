#!/usr/bin/env python3
""""Provide a tkinter GUI framework with main menu and main window.

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
from pywriter.yw.yw7_file import Yw7File


class MainTk(Ui):
    """A tkinter GUI root class.

    Public methods:
        start() -- start the Tk main loop.
        select_project(self, fileName) -- return a project file path.
        open_project(fileName) -- create a yWriter project instance and read the file.
        ask_yes_no(text) -- query yes or no with a pop-up box.
        set_info_how(message) -- show how the converter is doing.
        show_status(message) -- put text on the status bar.
        on_quit(event=None) -- save keyword arguments before exiting the program.
        
    Public instance variables: 
        kwargs -- keyword arguments buffer.
        ywPrj -- yWriter project to work with.
        root -- tk root window.

    Main menu, title bar, main window frame, status bar, path bar.
    """
    _KEY_RESTORE_STATUS = ('<Escape>', 'Esc')
    _KEY_OPEN_PROJECT = ('<Control-o>', 'Ctrl-O')
    _KEY_QUIT_PROGRAM = ('<Control-q>', 'Ctrl-Q')
    _YW_CLASS = Yw7File

    def __init__(self, title, **kwargs):
        """Initialize the GUI window and instance variables.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
         
        Required keyword arguments:
            yw_last_open -- str: initial file.
            root_geometry -- str: geometry of the root window.
        
        Operation:
        - Create a main menu to be extended by subclasses.
        - Create a title bar for the project title.
        - Open a main window frame to be used by subclasses.
        - Create a status bar to be used by subclasses.
        - Create a path bar for the project file path.
        
        Extends the superclass constructor.
        """
        super().__init__(title)
        self._fileTypes = [('yWriter 7 project', '.yw7')]
        self._title = title
        self._statusText = ''
        self.kwargs = kwargs
        self.ywPrj = None
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.title(title)
        if kwargs['root_geometry']:
            self.root.geometry(kwargs['root_geometry'])
        self._mainMenu = tk.Menu(self.root)

        self._build_main_menu()
        # Hook for subclasses

        self.root.config(menu=self._mainMenu)
        self._mainWindow = tk.Frame()
        self._mainWindow.pack(expand=True, fill='both')
        self._statusBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=2)
        self._statusBar.pack(expand=False, fill='both')
        self._pathBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=3)
        self._pathBar.pack(expand=False, fill='both')

        #--- Event bindings.
        self.root.bind(self._KEY_RESTORE_STATUS[0], self._restore_status)
        self.root.bind(self._KEY_OPEN_PROJECT[0], self._open_project)
        self.root.bind(self._KEY_QUIT_PROGRAM[0], self.on_quit)

    def _build_main_menu(self):
        """Add main menu entries.
        
        This is a template method that can be overridden by subclasses. 
        """
        self._fileMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='File', underline=0, menu=self._fileMenu)
        self._fileMenu.add_command(label='Open...', underline=0, accelerator=self._KEY_OPEN_PROJECT[1], command=lambda: self.open_project(''))
        self._fileMenu.add_command(label='Close', underline=0, command=self._close_project)
        self._fileMenu.entryconfig('Close', state='disabled')
        self._fileMenu.add_command(label='Exit', underline=1, accelerator=self._KEY_QUIT_PROGRAM[1], command=self.on_quit)

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self._fileMenu.entryconfig('Close', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self._fileMenu.entryconfig('Close', state='normal')

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def select_project(self, fileName):
        """Return a project file path.

        Positional arguments:
            fileName -- str: project file path.
            
        Optional arguments:
            fileTypes -- list of tuples for file selection (display text, extension).

        Priority:
        1. use file name argument
        2. open file select dialog

        On error, return an empty string.
        """
        initDir = os.path.dirname(self.kwargs['yw_last_open'])
        if not initDir:
            initDir = './'
        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(filetypes=self._fileTypes, defaultextension='.yw7', initialdir=initDir)
        if not fileName:
            return ''

        return fileName

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.

        Positional arguments:
            fileName -- str: project file path.
            
        Display project title and file path.
        Return True on success, otherwise return False.
        To be extended by subclasses.
        """
        self.show_status(self._statusText)
        fileName = self.select_project(fileName)
        if not fileName:
            return False

        if self.ywPrj is not None:
            self._close_project()
        self.kwargs['yw_last_open'] = fileName
        self.ywPrj = self._YW_CLASS(fileName)
        message = self.ywPrj.read()
        if message.startswith(ERROR):
            self._close_project()
            self.set_info_how(message)
            return False

        self._show_path(f'{os.path.normpath(self.ywPrj.filePath)}')
        if self.ywPrj.title:
            titleView = self.ywPrj.title
        else:
            titleView = 'Untitled yWriter project'
        if self.ywPrj.authorName:
            authorView = self.ywPrj.authorName
        else:
            authorView = 'Unknown author'
        self.root.title(f'{titleView} by {authorView} - {self._title}')
        self._enable_menu()
        return True

    def _open_project(self, event=None):
        """Create a yWriter project instance and read the file.
        
        This non-public method is meant for event handling.
        """
        self.open_project('')

    def _close_project(self, event=None):
        """Close the yWriter project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        self.ywPrj = None
        self.root.title(self._title)
        self.show_status('')
        self._show_path('')
        self._disable_menu()

    def ask_yes_no(self, text):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Overrides the superclass method.       
        """
        return messagebox.askyesno(self._title, text)

    def set_info_how(self, message):
        """Show how the converter is doing.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Display the message at the status bar.
        Overrides the superclass method.
        """
        if message.startswith(ERROR):
            self._statusBar.config(bg='red')
            self._statusBar.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()
        else:
            self._statusBar.config(bg='green')
            self._statusBar.config(fg='white')
            self.infoHowText = message
        self._statusBar.config(text=self.infoHowText)

    def show_status(self, message):
        """Put text on the status bar."""
        self._statusText = message
        self._statusBar.config(bg=self.root.cget('background'))
        self._statusBar.config(fg='black')
        self._statusBar.config(text=message)

    def _show_path(self, message):
        """Put text on the path bar."""
        self._pathText = message
        self._pathBar.config(text=message)

    def _restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.show_status(self._statusText)

    def on_quit(self, event=None):
        """Save keyword arguments before exiting the program."""
        self.kwargs['root_geometry'] = self.root.winfo_geometry()
        self.root.quit()
