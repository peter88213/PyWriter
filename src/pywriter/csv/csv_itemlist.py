"""Provide a class for csv item list import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.world_element import WorldElement


class CsvItemList(CsvFile):
    """csv file representation of a yWriter project's items table. 
    """

    DESCRIPTION = 'Item list'
    SUFFIX = '_itemlist'

    rowTitles = ['ID', 'Name', 'Description', 'Aka', 'Tags']

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the WorldElement attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        Extend the superclass method.
        """
        message = super().read()

        if message.startswith('ERROR'):
            return message

        for cells in self.rows:

            if 'ItID:' in cells[0]:
                itId = re.search('ItID\:([0-9]+)', cells[0]).group(1)
                self.srtItems.append(itId)
                self.items[itId] = WorldElement()
                self.items[itId].title = cells[1]
                self.items[itId].desc = self.convert_to_yw(cells[2])
                self.items[itId].aka = cells[3]
                self.items[itId].tags = self.get_list(cells[4])

        return 'SUCCESS: Data read from "{}".'.format(os.path.normpath(self.filePath))
