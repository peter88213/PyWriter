"""Provide a class for csv location list import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.world_element import WorldElement


class CsvLocList(CsvFile):
    """csv file representation of an yWriter project's locations table. 

    Represents a csv file with a record per location.
    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR location.
    """

    DESCRIPTION = 'Location list'
    SUFFIX = '_loclist'

    fileHeader = '''ID|Name|Description|Aka|Tags
'''

    locationTemplate = '''LcID:$ID|$Title|"$Desc"|$AKA|$Tags
'''

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the WorldElement attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        message = CsvFile.read(self)

        if message.startswith('ERROR'):
            return message

        for cells in self.rows:

            if 'LcID:' in cells[0]:
                lcId = re.search('LcID\:([0-9]+)', cells[0]).group(1)
                self.srtLocations.append(lcId)
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = cells[1]
                self.locations[lcId].desc = self.convert_to_yw(cells[2])
                self.locations[lcId].aka = cells[3]
                self.locations[lcId].tags = self.get_list(cells[4])

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

    def merge(self, novel):
        """Copy required attributes of the novel object.
        Return a message beginning with SUCCESS or ERROR.
        """
        self.srtLocations = novel.srtLocations
        self.locations = novel.locations
        return 'SUCCESS'
