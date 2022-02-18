"""Provide a class for csv plot list import.

Convention: 
* Used chapters marked "other" precede and describe plot sections (e.g. acts, steps).
* Tagged scenes contain plot events (e.g. inciting event, plot point, climax).
* Scene notes give plot relevant informations.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from pywriter.pywriter_globals import ERROR
from pywriter.csv.csv_file import CsvFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class CsvPlotList(CsvFile):
    """csv file representation of a yWriter project's scenes table. 
    """

    DESCRIPTION = 'Plot list'
    SUFFIX = '_plotlist'

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    _NOT_APPLICABLE = 'N/A'
    # Scene field column header for fields not being assigned to a storyline

    _rowTitles = ['ID', 'Plot section', 'Plot event', 'Scene title', 'Details', 'Scene', 'Words total',
                 '$FieldTitle1', '$FieldTitle2', '$FieldTitle3', '$FieldTitle4']

    def read(self):
        """Parse the csv file located at filePath, fetching 
        the Scene attributes contained.
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        """
        message = super().read()

        if message.startswith(ERROR):
            return message

        tableHeader = self._rows[0]

        for cells in self._rows:

            if 'ChID:' in cells[0]:
                chId = re.search('ChID\:([0-9]+)', cells[0]).group(1)
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = cells[1]
                self.chapters[chId].desc = self._convert_to_yw(cells[4])

            if 'ScID:' in cells[0]:
                scId = re.search('ScID\:([0-9]+)', cells[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].tags = self._get_list(cells[2])
                self.scenes[scId].title = cells[3]
                self.scenes[scId].sceneNotes = self._convert_to_yw(cells[4])

                i = 5
                # Don't write back sceneCount
                i += 1
                # Don't write back wordCount
                i += 1

                # Transfer scene ratings; set to 1 if deleted

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field1 = cells[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field1 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field2 = cells[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field2 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field3 = cells[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field3 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field4 = cells[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field4 = '1'

        return 'CSV data converted to novel structure.'
