"""Provide a generic class for csv file import.

Other csv file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv
from pywriter.pywriter_globals import *
from pywriter.model.novel import Novel


class CsvFile(Novel):
    """csv file representation.

    Public methods:
        read() -- parse the file and get the instance variables.

    Convention:
    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """
    EXTENSION = '.csv'
    # overwrites Novel.EXTENSION
    _SEPARATOR = ','
    # delimits data fields within a record.
    _rowTitles = []

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._rows = []

    def read(self):
        """Parse the file and get the instance variables.
        
        Parse the csv file located at filePath, fetching the rows.
        Check the number of fields in each row.
        Return a message beginning with the ERROR constant in case of error.
        Overrides the superclass method.
        """
        self._rows = []
        cellsPerRow = len(self._rowTitles)
        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self._SEPARATOR)
                for row in reader:
                    if len(row) != cellsPerRow:
                        return f'{ERROR}{MSG_WRONG_CSV_STRUCTURE}.'

                    self._rows.append(row)
        except(FileNotFoundError):
            return f'{ERROR}{MSG_NOT_FOUND}: "{os.path.normpath(self.filePath)}".'

        except:
            return f'{ERROR}{MSG_CANNOT_PARSE}: "{os.path.normpath(self.filePath)}".'

        return 'CSV data read in.'

    def _get_list(self, text):
        """Convert a string into a list.
        
        Positional arguments:
            text -- string containing comma-separated substrings.
        
        Split a sequence of comma separated strings into a list of strings.
        Remove leading and trailing spaces, if any.
        Return a list of strings.
        """
        elements = []
        tempList = text.split(',')
        for element in tempList:
            elements.append(element.strip())
        return elements
