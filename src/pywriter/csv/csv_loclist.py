"""CsvLocList - Class for csv locations table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.object import Object


class CsvLocList(CsvFile):
    """csv file representation of an yWriter project's locations table. 

    Represents a csv file with a record per location.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR location.
    """

    DESCRIPTION = 'Location list'
    SUFFIX = '_loclist'

    fileHeader = '''ID|Name|Description|Aka|Tags
'''

    locationTemplate = '''LcID:$ID|$Title|$Desc|$AKA|$Tags
'''

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Object attributes contained.
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

            if 'LcID:' in cell[0]:
                lcId = re.search('LcID\:([0-9]+)', cell[0]).group(1)
                self.locations[lcId] = Object()
                self.locations[lcId].title = cell[1]
                self.locations[lcId].desc = self.convert_to_yw(cell[2])
                self.locations[lcId].aka = cell[3]
                self.locations[lcId].tags = cell[4].split(';')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """
        self.locations = novel.locations
