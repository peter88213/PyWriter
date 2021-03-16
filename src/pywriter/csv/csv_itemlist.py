"""CsvItemList - Class for csv items table.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.world_element import WorldElement


class CsvItemList(CsvFile):
    """csv file representation of an yWriter project's items table. 

    Represents a csv file with a record per item.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR item.
    """

    DESCRIPTION = 'Item list'
    SUFFIX = '_itemlist'

    fileHeader = '''ID|Name|Description|Aka|Tags
'''

    itemTemplate = '''ItID:$ID|$Title|"$Desc"|$AKA|$Tags
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

            if 'ItID:' in cells[0]:
                itId = re.search('ItID\:([0-9]+)', cells[0]).group(1)
                self.srtItems.append(itId)
                self.items[itId] = WorldElement()
                self.items[itId].title = cells[1]
                self.items[itId].desc = self.convert_to_yw(cells[2])
                self.items[itId].aka = cells[3]
                self.items[itId].tags = cells[4].split(';')

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

    def merge(self, novel):
        """Copy required attributes of the novel object.
        Return a message beginning with SUCCESS or ERROR.
        """
        self.srtItems = novel.srtItems
        self.items = novel.items
        return 'SUCCESS'
