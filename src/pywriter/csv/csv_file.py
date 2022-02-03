"""Provide a generic class for csv file import.

Other csv file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv

from pywriter.pywriter_globals import ERROR
from pywriter.model.novel import Novel


class CsvFile(Novel):
    """csv file representation.

    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    # overwrites Novel.EXTENSION

    _SEPARATOR = ','
    # delimits data fields within a record.

    _rowTitles = []

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)
        self._rows = []
        
        
    def read(self):
        """Parse the csv file located at filePath, fetching the _rows.
        Check the number of fields in each row.
        Return a message beginning with the ERROR constant in case of error.
        Override the superclass method.
        """
        self._rows = []
        cellsPerRow = len(self._rowTitles)

        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self._SEPARATOR)

                for row in reader:
                    # Each row read from the csv file is returned
                    # as a list of strings

                    if len(row) != cellsPerRow:
                        return f'{ERROR}Wrong csv structure.'

                    self._rows.append(row)

        except(FileNotFoundError):
            return f'{ERROR}"{os.path.normpath(self.filePath)}" not found.'

        except:
            return f'{ERROR}Can not parse "{os.path.normpath(self.filePath)}".'

        return 'CSV data read in.'

    def _get_list(self, text):
        """Split a sequence of comma separated strings into a list of strings.
        Remove leading and trailing spaces, if any.
        """
        elements = []
        tempList = text.split(',')

        for element in tempList:
            elements.append(element.strip())

        return elements
