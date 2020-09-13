"""CsvCharList - Class for csv characters table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.character import Character


class CsvCharList(CsvFile):
    """csv file representation of an yWriter project's characters table. 

    Represents a csv file with a record per character.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    DESCRIPTION = 'Character list'
    SUFFIX = '_charlist'

    fileHeader = '''ID|Name|Full name|Aka|Description|Bio|Goals|Importance|Tags|Notes
'''

    characterTemplate = '''CrID:$ID|$Title|$FullName|$AKA|$Desc|$Bio|$Goals|$Status|$Tags|$Notes
'''

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Character attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                lines = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self._filePath) + '" not found.'

        if lines[0] != self.fileHeader:
            return 'ERROR: Wrong lines content.'

        cellsInLine = len(self.fileHeader.split(self._SEPARATOR))

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
                self.characters[crId].desc = self.convert_to_yw(cell[4])
                self.characters[crId].bio = cell[5]
                self.characters[crId].goals = cell[6]

                if Character.MAJOR_MARKER in cell[7]:
                    self.characters[crId].isMajor = True

                else:
                    self.characters[crId].isMajor = False

                self.characters[crId].tags = cell[8].split(';')
                self.characters[crId].notes = self.convert_to_yw(cell[9])

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """
        self.characters = novel.characters
