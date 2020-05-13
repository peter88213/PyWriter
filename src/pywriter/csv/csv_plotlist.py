"""CsvPlotList - Class for csv plot structure table.

Convention: 
* Used chapters marked "other" precede and describe plot sections (e.g. acts, steps).
* Tagged scenes contain plot events (e.g. inciting event, plot point, climax).
* Scene notes give plot relevant informations.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene

PLOTLIST_SUFFIX = '_plotlist.csv'
MANUSCRIPT_SUFFIX = '_manuscript.odt'


class CsvPlotList(Novel):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites Novel._FILE_EXTENSION
    _FILE_SUFFIX = '_plot'

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    _TABLE_HEADER = ('ID'
                     + _SEPARATOR
                     + 'Plot section'
                     + _SEPARATOR
                     + 'Plot event'
                     + _SEPARATOR
                     + 'Plot event title'
                     + _SEPARATOR
                     + 'Details'
                     + '\n')

    def read(self):
        """Parse the csv file located at filePath, fetching 
        the Scene attributes contained.
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

            if 'ChID:' in cell[0]:
                chId = re.search('ChID\:([0-9]+)', cell[0]).group(1)
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = cell[1]
                self.chapters[chId].desc = cell[4].replace(
                    self._LINEBREAK, '\n')

            if 'ScID:' in cell[0]:
                scId = re.search('ScID\:([0-9]+)', cell[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].tags = cell[2].split(';')
                self.scenes[scId].title = cell[3]
                self.scenes[scId].sceneNotes = cell[4].replace(
                    self._LINEBREAK, '\n')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def write(self, novel):
        """Generate a csv file showing the novel's plot structure.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the chapter/scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        odtPath = os.path.realpath(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(PLOTLIST_SUFFIX, MANUSCRIPT_SUFFIX)

        # first record: the table's column headings

        table = [self._TABLE_HEADER]

        # Add a record for each used scene in a regular chapter
        # and for each chapter marked "Other".

        for chId in self.srtChapters:

            if not self.chapters[chId].isUnused:

                if self.chapters[chId].chType == 1:
                    # Chapter marked "Other" precedes and describes a Plot section.
                    # Put chapter description to "details".

                    if self.chapters[chId].desc is None:
                        self.chapters[chId].desc = ''

                    table.append('ChID:' + chId
                                 + self._SEPARATOR
                                 + self.chapters[chId].title
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self.chapters[chId].desc.rstrip().replace('\n', self._LINEBREAK)
                                 + '\n')

                else:
                    for scId in self.chapters[chId].srtScenes:

                        if not self.scenes[scId].isUnused:
                            # If the scene contains plot information:
                            # a tag marks the plot event (e.g. inciting event, plot point, climax).
                            # Put scene note text to "details".

                            if self.scenes[scId].sceneNotes is None:
                                self.scenes[scId].sceneNotes = ''

                            if self.scenes[scId].tags is None:
                                self.scenes[scId].tags = ['']

                            table.append('=HYPERLINK("file:///'
                                         + odtPath + '#ScID:' + scId + '%7Cregion";"ScID:' + scId + '")'
                                         + self._SEPARATOR
                                         + self._SEPARATOR
                                         + ';'.join(self.scenes[scId].tags)
                                         + self._SEPARATOR
                                         + self.scenes[scId].title
                                         + self._SEPARATOR
                                         + self.scenes[scId].sceneNotes.rstrip().replace('\n', self._LINEBREAK)
                                         + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self):
        return None
