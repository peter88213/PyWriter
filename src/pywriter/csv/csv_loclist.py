"""CsvLocList - Class for csv locations table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.model.novel import Novel
from pywriter.model.object import Object


class CsvLocList(Novel):
    """csv file representation of an yWriter project's locations table. 

    Represents a csv file with a record per location.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR location.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites Novel._FILE_EXTENSION

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    _TABLE_HEADER = ('ID'
                     + _SEPARATOR
                     + 'Name'
                     + _SEPARATOR
                     + 'Description'
                     + _SEPARATOR
                     + 'Aka'
                     + _SEPARATOR
                     + 'Tags'
                     + '\n')

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Object attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                lines = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        if lines[0] != self._TABLE_HEADER:
            return 'ERROR: Wrong lines content.'

        cellsInLine = len(self._TABLE_HEADER.split(self._SEPARATOR))

        for line in lines:
            cell = line.rstrip().split(self._SEPARATOR)

            if len(cell) != cellsInLine:
                return 'ERROR: Wrong cell structure.'

            if 'LcID:' in cell[0]:
                lcId = re.search('LcID\:([0-9]+)', cell[0]).group(1)
                self.locations[lcId] = Object()
                self.locations[lcId].title = cell[1]
                self.locations[lcId].desc = cell[2].replace(
                    self._LINEBREAK, '\n')
                self.locations[lcId].aka = cell[3]
                self.locations[lcId].tags = cell[4].split(';')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """
        self.locations = novel.locations

    def write(self):
        """Generate a csv file containing per location:
        - location ID, 
        - location title,
        - location description, 
        - location alternative name, 
        - location tags.
        Return a message beginning with SUCCESS or ERROR.
        """

        # first record: the table's column headings

        table = [self._TABLE_HEADER]

        # Add a record for each location

        for lcId in self.locations:

            if self.locations[lcId].desc is None:
                self.locations[lcId].desc = ''

            if self.locations[lcId].aka is None:
                self.locations[lcId].aka = ''

            if self.locations[lcId].tags is None:
                self.locations[lcId].tags = ['']

            table.append('LcID:' + str(lcId)
                         + self._SEPARATOR
                         + self.locations[lcId].title
                         + self._SEPARATOR
                         + self.locations[lcId].desc.rstrip().replace('\n', self._LINEBREAK)
                         + self._SEPARATOR
                         + self.locations[lcId].aka
                         + self._SEPARATOR
                         + ';'.join(self.locations[lcId].tags)
                         + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self):
        """This file format has no comparable structure."""
        return None
