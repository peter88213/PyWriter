"""PlotList - Class for csv plot structure table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.model.novel import Novel
from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene

SEPARATOR = '|'     # delimits data fields within a record.
LINEBREAK = '\t'    # substitutes embedded line breaks.


class PlotList(PywFile):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the SEPARATOR character.

    # Attributes

    _text : str
        contains the parsed data.

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    read : str
        parse the csv file located at filePath, fetching 
        the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a csv file
        Return a message beginning with SUCCESS or ERROR.

    get_structure : None
        Return None to prevent structural comparison.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites PywFile._FILE_EXTENSION
    _FILE_SUFFIX = '_plot'

    def read(self) -> str:
        """Read data from a csv file containing scene attributes. """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                table = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        for record in table:
            field = record.split(SEPARATOR)

            if 'ChID:' in field[0]:
                chId = re.search('ChID\:([0-9]+)', field[0]).group(1)
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = field[1]
                self.chapters[chId].desc = field[4].replace(LINEBREAK, '\n')

            if 'ScID:' in field[0]:
                scId = re.search('ScID\:([0-9]+)', field[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].tags = field[2].split(';')
                self.scenes[scId].title = field[3]
                self.scenes[scId].desc = field[4].replace(LINEBREAK, '\n')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Write scene attributes to csv file. """

        # Copy the scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        odtPath = os.path.realpath(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace('_plot.csv', '_manuscript.odt')

        # first record: the table's column headings

        table = ['ID'
                 + SEPARATOR
                 + 'Plot section'
                 + SEPARATOR
                 + 'Plot event'
                 + SEPARATOR
                 + 'Plot event title'
                 + SEPARATOR
                 + 'Details'
                 + '\n']

        # Add a record for each used scene in a regular chapter

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused):

                if self.chapters[chId].chType == 1:

                    if self.chapters[chId].desc is not None:
                        chapterDesc = self.chapters[chId].desc.rstrip(
                        ).replace('\n', LINEBREAK)

                    else:
                        chapterDesc = ''

                    table.append('ChID:' + chId
                                 + SEPARATOR
                                 + self.chapters[chId].title
                                 + SEPARATOR
                                 + SEPARATOR
                                 + SEPARATOR
                                 + chapterDesc
                                 + '\n')

                else:
                    for scId in self.chapters[chId].srtScenes:

                        if (not self.scenes[scId].isUnused) and (self.scenes[scId].tags != [] or self.scenes[scId].sceneNotes != ''):

                            if self.scenes[scId].sceneNotes is not None:
                                sceneNotes = self.scenes[scId].sceneNotes.rstrip(
                                ).replace('\n', LINEBREAK)

                            else:
                                sceneNotes = ''

                            table.append('=HYPERLINK("file:///'
                                         + odtPath + '#ScID:' + scId + '";"ScID:' + scId + '")'
                                         + SEPARATOR
                                         + SEPARATOR
                                         + ';'.join(self.scenes[scId].tags)
                                         + SEPARATOR
                                         + self.scenes[scId].title
                                         + SEPARATOR
                                         + sceneNotes
                                         + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self) -> None:
        return None
