"""CsvCharList - Class for csv characters table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
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

    characterTemplate = '''CrID:$ID|$Title|$FullName|$AKA|"$Desc"|"$Bio"|"$Goals"|$Status|$Tags|"$Notes"
'''

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Character attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        message = CsvFile.read(self)

        if message.startswith('ERROR'):
            return message

        for cells in self.rows:

            if 'CrID:' in cells[0]:
                crId = re.search('CrID\:([0-9]+)', cells[0]).group(1)
                self.srtCharacters.append(crId)
                self.characters[crId] = Character()
                self.characters[crId].title = cells[1]
                self.characters[crId].fullName = cells[2]
                self.characters[crId].aka = cells[3]
                self.characters[crId].desc = self.convert_to_yw(cells[4])
                self.characters[crId].bio = cells[5]
                self.characters[crId].goals = cells[6]

                if Character.MAJOR_MARKER in cells[7]:
                    self.characters[crId].isMajor = True

                else:
                    self.characters[crId].isMajor = False

                self.characters[crId].tags = cells[8].split(';')
                self.characters[crId].notes = self.convert_to_yw(cells[9])

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

    def merge(self, novel):
        """Copy required attributes of the novel object.
        Return a message beginning with SUCCESS or ERROR.
        """
        self.srtCharacters = novel.srtCharacters
        self.characters = novel.characters
        return 'SUCCESS'
