"""Provide a class for csv location list import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from pywriter.pywriter_globals import ERROR
from pywriter.csv.csv_file import CsvFile
from pywriter.model.world_element import WorldElement


class CsvLocList(CsvFile):
    """csv file representation of a yWriter project's locations table. 
    """

    DESCRIPTION = 'Location list'
    SUFFIX = '_loclist'

    rowTitles = ['ID', 'Name', 'Description', 'Aka', 'Tags']

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the WorldElement attributes contained.
        Return a message beginning with the ERROR constant in case of error.
        Extend the superclass method.
        """
        message = super().read()

        if message.startswith(ERROR):
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

        return 'Location data read in.'
