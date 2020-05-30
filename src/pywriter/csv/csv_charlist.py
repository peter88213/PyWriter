"""CsvCharList - Class for csv characters table.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.model.novel import Novel
from pywriter.model.character import Character


class CsvCharList(Novel):
    """csv file representation of an yWriter project's characters table. 

    Represents a csv file with a record per character.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites Novel._FILE_EXTENSION

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    _TABLE_HEADER = ('ID'
                     + _SEPARATOR
                     + 'Name'
                     + _SEPARATOR
                     + 'Full name'
                     + _SEPARATOR
                     + 'Aka'
                     + _SEPARATOR
                     + 'Description'
                     + _SEPARATOR
                     + 'Bio'
                     + _SEPARATOR
                     + 'Goals'
                     + _SEPARATOR
                     + 'Importance'
                     + _SEPARATOR
                     + 'Tags'
                     + _SEPARATOR
                     + 'Notes'
                     + '\n')

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Character attributes contained.
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

            if 'CrID:' in cell[0]:
                crId = re.search('CrID\:([0-9]+)', cell[0]).group(1)
                self.characters[crId] = Character()
                self.characters[crId].title = cell[1]
                self.characters[crId].fullName = cell[2]
                self.characters[crId].aka = cell[3]
                self.characters[crId].desc = cell[4].replace(
                    self._LINEBREAK, '\n')
                self.characters[crId].bio = cell[5]
                self.characters[crId].goals = cell[6]

                if 'Major' in cell[7]:
                    self.characters[crId].isMajor = True

                else:
                    self.characters[crId].isMajor = False

                self.characters[crId].tags = cell[8].split(';')
                self.characters[crId].notes = cell[9].replace(
                    self._LINEBREAK, '\n')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        if novel.characters is not None:
            self.characters = novel.characters

    def write(self):
        """Generate a csv file containing per character:
        - character ID, 
        - character name,
        - character full name,
        - character alternative name, 
        - character description, 
        - character bio,
        - character goals,
        - character importance,
        - character tags,
        - character notes.
        Return a message beginning with SUCCESS or ERROR.
        """

        def importance(isMajor):

            if isMajor:
                return 'Major'

            else:
                return 'Minor'

        # first record: the table's column headings

        table = [self._TABLE_HEADER]

        # Add a record for each character

        for crId in self.characters:

            if self.characters[crId].fullName is None:
                self.characters[crId].fullName = ''

            if self.characters[crId].aka is None:
                self.characters[crId].aka = ''

            if self.characters[crId].desc is None:
                self.characters[crId].desc = ''

            if self.characters[crId].bio is None:
                self.characters[crId].bio = ''

            if self.characters[crId].goals is None:
                self.characters[crId].goals = ''

            if self.characters[crId].isMajor is None:
                self.characters[crId].isMajor = False

            if self.characters[crId].tags is None:
                self.characters[crId].tags = ['']

            if self.characters[crId].notes is None:
                self.characters[crId].notes = ''

            table.append('CrID:' + str(crId)
                         + self._SEPARATOR
                         + self.characters[crId].title
                         + self._SEPARATOR
                         + self.characters[crId].fullName
                         + self._SEPARATOR
                         + self.characters[crId].aka
                         + self._SEPARATOR
                         + self.characters[crId].desc.rstrip().replace('\n', self._LINEBREAK)
                         + self._SEPARATOR
                         + self.characters[crId].bio
                         + self._SEPARATOR
                         + self.characters[crId].goals
                         + self._SEPARATOR
                         + importance(self.characters[crId].isMajor)
                         + self._SEPARATOR
                         + ';'.join(self.characters[crId].tags)
                         + self._SEPARATOR
                         + self.characters[crId].notes.rstrip().replace('\n', self._LINEBREAK)
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
