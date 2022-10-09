""""Provide a tkinter GUI framework with main menu and main window.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pywriter.pywriter_globals import *
from pywriter.ui.ui import Ui
from pywriter.yw.yw7_file import Yw7File


class MainTk(Ui):
    """A tkinter GUI root class.

    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        start() -- start the Tk main loop.
        select_project(self, fileName) -- return a project file path.
        open_project(fileName) -- create a yWriter project instance and read the file.
        close_project() -- close the yWriter project without saving and reset the user interface.
        ask_yes_no(text) -- query yes or no with a pop-up box.
        set_info_how(message) -- show how the converter is doing.
        show_status(message) -- put text on the status bar.
        show_path(message) -- put text on the path bar."
        restore_status() -- overwrite error message with the status before.
        on_quit() -- save keyword arguments before exiting the program.
        show_warning(message) -- Display a warning message box.
        
    Public instance variables: 
        title -- str: Application title.
        statusText -- str: Text to be displayed at the status bar.
        kwargs -- keyword arguments buffer.
        ywPrj -- yWriter project to work with.
        root -- tk top level window.
        mainMenu -- top level menubar.
        mainWindow -- tk frame in the top level window.
        statusBar -- tk label in the top level window.
        pathBar -- tk label in the top level window.
        fileMenu -- "File" submenu in main menu. 
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
        self._fileTypes = [(_('yWriter 7 project'), '.yw7')]
        self.title = title
        self._statusText = ''
        self.kwargs = kwargs
        self.ywPrj = None
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.title(title)
        if kwargs['root_geometry']:
            self.root.geometry(kwargs['root_geometry'])
        self.mainMenu = tk.Menu(self.root)

        self._build_main_menu()
        # Hook for subclasses

        self.root.config(menu=self.mainMenu)
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both')
        self.statusBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=2)
        self.statusBar.pack(expand=False, fill='both')
        self.pathBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=3)
        self.pathBar.pack(expand=False, fill='both')

        #--- Event bindings.
        self.root.bind(self._KEY_RESTORE_STATUS[0], self.restore_status)
        self.root.bind(self._KEY_OPEN_PROJECT[0], self._open_project)
        self.root.bind(self._KEY_QUIT_PROGRAM[0], self.on_quit)

    def _build_main_menu(self):
        """Add main menu entries.
        
        This is a template method that can be overridden by subclasses. 
        """
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('File'), menu=self.fileMenu)
        self.fileMenu.add_command(label=_('Open...'), accelerator=self._KEY_OPEN_PROJECT[1], command=lambda: self.open_project(''))
        self.fileMenu.add_command(label=_('Close'), command=self.close_project)
        self.fileMenu.entryconfig(_('Close'), state='disabled')
        self.fileMenu.add_command(label=_('Exit'), accelerator=self._KEY_QUIT_PROGRAM[1], command=self.on_quit)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig(_('Close'), state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self.fileMenu.entryconfig(_('Close'), state='normal')

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
            self.close_project()
        self.kwargs['yw_last_open'] = fileName
        self.ywPrj = self._YW_CLASS(fileName)
        message = self.ywPrj.read()
        if message.startswith(ERROR):
            self.close_project()
            self.set_info_how(message)
            return False

        self.show_path(f'{os.path.normpath(self.ywPrj.filePath)}')
        self.set_title()
        self.enable_menu()
        return True

    def set_title(self):
        """Set the main window title. 
        
        'Document title by author - application'
        """
        if self.ywPrj.title:
            titleView = self.ywPrj.title
        else:
            titleView = _('Untitled project')
        if self.ywPrj.authorName:
            authorView = self.ywPrj.authorName
        else:
            authorView = _('Unknown author')
        self.root.title(f'{titleView} {_("by")} {authorView} - {self.title}')

    def _open_project(self, event=None):
        """Create a yWriter project instance and read the file.
        
        This non-public method is meant for event handling.
        """
        self.open_project('')

    def close_project(self, event=None):
        """Close the yWriter project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        self.ywPrj = None
        self.root.title(self.title)
        self.show_status('')
        self.show_path('')
        self.disable_menu()

    def ask_yes_no(self, text):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Overrides the superclass method.       
        """
        return messagebox.askyesno(self.title, text)

    def set_info_how(self, message):
        """Show how the converter is doing.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Display the message at the status bar.
        Overrides the superclass method.
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

    def show_status(self, message):
        """Put text on the status bar."""
        self._statusText = message
        self.statusBar.config(bg=self.root.cget('background'))
        self.statusBar.config(fg='black')
        self.statusBar.config(text=message)

    def show_path(self, message):
        """Put text on the path bar."""
        self._pathText = message
        self.pathBar.config(text=message)

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.show_status(self._statusText)

    def on_quit(self, event=None):
        """Save keyword arguments before exiting the program."""
        self.kwargs['root_geometry'] = self.root.winfo_geometry()
        self.root.quit()

    def show_warning(self, message):
        """Display a warning message box."""
        messagebox.showwarning(self.title, message)
