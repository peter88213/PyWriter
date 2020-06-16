"""CsvItemList - Class for csv items table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.model.novel import Novel
from pywriter.model.object import Object


class CsvItemList(Novel):
    """csv file representation of an yWriter project's items table. 

    Represents a csv file with a record per item.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR item.
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

            if 'ItID:' in cell[0]:
                itId = re.search('ItID\:([0-9]+)', cell[0]).group(1)
                self.items[itId] = Object()
                self.items[itId].title = cell[1]
                self.items[itId].desc = cell[2].replace(
                    self._LINEBREAK, '\n')
                self.items[itId].aka = cell[3]
                self.items[itId].tags = cell[4].split(';')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        if novel.items is not None:
            self.items = novel.items

    def write(self):
        """Generate a csv file containing per item:
        - item ID, 
        - item title,
        - item description, 
        - item alternative name, 
        - item tags.
        Return a message beginning with SUCCESS or ERROR.
        """

        # first record: the table's column headings

        table = [self._TABLE_HEADER]

        # Add a record for each item

        for itId in self.items:

            if self.items[itId].desc is None:
                self.items[itId].desc = ''

            if self.items[itId].aka is None:
                self.items[itId].aka = ''

            if self.items[itId].tags is None:
                self.items[itId].tags = ['']

            table.append('ItID:' + str(itId)
                         + self._SEPARATOR
                         + self.items[itId].title
                         + self._SEPARATOR
                         + self.items[itId].desc.rstrip().replace('\n',
                                                                  self._LINEBREAK)
                         + self._SEPARATOR
                         + self.items[itId].aka
                         + self._SEPARATOR
                         + ';'.join(self.items[itId].tags)
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
