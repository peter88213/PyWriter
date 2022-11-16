""""Provide a tkinter GUI framework for converter applications.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.pywriter_globals import *
from pywriter.ui.main_tk import MainTk
from pywriter.yw.yw7_file import Yw7File


class MainTkCnv(MainTk):
    """A tkinter GUI base class for yWriter file conversion.

    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        open_project(fileName) -- select a valid project file and display the path.
        reverse_direction() -- swap source and target file names.
        convert_file() -- call the converter's conversion method, if a source file is selected.

    Public instance variables:
        converter -- converter strategy class.

    Adds a "Swap" and a "Run" entry to the main menu.
    """
    _EXPORT_DESC = 'Export from yWriter.'
    _IMPORT_DESC = 'Import to yWriter.'

    def __init__(self, title, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
                    
        Required keyword arguments:
            yw_last_open -- initial file.
            file_types -- list of tuples for file selection (display text, extension).
        
        Extends the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self._fileTypes = kwargs['file_types']
        self.converter = None
        self._sourcePath = None
        self._ywExtension = Yw7File.EXTENSION
        self._docExtension = None

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self.mainMenu.add_command(label=_('Swap'), command=self.reverse_direction)
        self.mainMenu.entryconfig(_('Swap'), state='disabled')
        self.mainMenu.add_command(label=_('Run'), command=self.convert_file)
        self.mainMenu.entryconfig(_('Run'), state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig(_('Run'), state='disabled')
        self.mainMenu.entryconfig(_('Swap'), state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig(_('Run'), state='normal')
        self.mainMenu.entryconfig(_('Swap'), state='normal')

    def open_project(self, fileName):
        """Select a valid project file and display the path.
        
        Positional arguments:
            fileName -- str: project file path.
            
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        fileName = super().select_project(fileName)
        if not fileName:
            return False
        self.kwargs['yw_last_open'] = fileName
        self._sourcePath = fileName
        self.enable_menu()
        if fileName.endswith(self._ywExtension):
            self.root.title(f'{self._EXPORT_DESC} - {self.title}')
        elif fileName.endswith(self._docExtension):
            self.root.title(f'{self._IMPORT_DESC} - {self.title}')
        self.show_path(f'{norm_path(fileName)}')
        return True

    def reverse_direction(self):
        """Swap source and target file names."""
        fileName, fileExtension = os.path.splitext(self._sourcePath)
        if fileExtension == self._ywExtension:
            self._sourcePath = f'{fileName}{self._docExtension}'
            self.show_path(norm_path(self._sourcePath))
            self.root.title(f'{self._IMPORT_DESC} - {self.title}')
            self.show_status('')
        elif fileExtension == self._docExtension:
            self._sourcePath = f'{fileName}{self._ywExtension}'
            self.show_path(norm_path(self._sourcePath))
            self.root.title(f'{self._EXPORT_DESC} - {self.title}')
            self.show_status('')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected."""
        self.show_status('')
        self.kwargs['yw_last_open'] = self._sourcePath
        self.converter.run(self._sourcePath, **self.kwargs)

