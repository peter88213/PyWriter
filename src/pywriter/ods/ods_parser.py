"""Provide a class for parsing ODS documents.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import zipfile
from xml import sax
from pywriter.pywriter_globals import *


class OdsParser(sax.ContentHandler):
    """An ODS document parser.
    
    Public methods:
        feed_file(filePath) -- Feed an ODS file to the parser.
           
      Methods overriding xml.sax.ContentHandler methods (not meant to be overridden by subclasses)
        startElement -- Signals the start of an element in non-namespace mode.
        endElement -- Signals the end of an element in non-namespace mode.
        characters -- Receive notification of character data.
    
    Return a list of rows, containing lists of column cells.
    The PyWriter csv import classes thus can be reused.
    """

    def __init__(self):
        super().__init__()
        self._rows = []
        self._cells = []
        self._inCell = None
        self.__cellsPerRow = 0

    def feed_file(self, filePath, cellsPerRow):
        """Feed an ODS file to the parser.
        
        Positional arguments:
            filePath -- str: ODS document path.
            cellsPerRow -- int: Number of cells per row.
        
        First unzip the ODS file located at self.filePath, 
        and get languageCode, countryCode, title, desc, and authorName,        
        Then call the sax parser for content.xml.
        """
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(filePath)}".')

        #--- Parse 'content.xml'.
        self._rows = []
        self._cells = []
        self._lines = []
        self._inCell = False
        self._cellsPerRow = cellsPerRow
        sax.parseString(content, self)
        return self._rows

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        if name == 'table:table-cell':
            self._inCell = True
        elif name == 'text:p':
            if self._lines:
                line = ''.join(self._lines)
                self._lines = [line.strip(), '\n']

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        if name == 'table:table-cell':
            if len(self._cells) < self._cellsPerRow:
                if self._lines:
                    cell = ''.join(self._lines)
                else:
                    cell = ''
                self._cells.append(cell.strip())
            self._inCell = False
            self._lines = []
        elif name == 'table:table-row':
            self._rows.append(self._cells)
            self._cells = []

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        if self._inCell:
            self._lines.append(content)

