"""SceneList - Class for csv scenes table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.model.novel import Novel
from pywriter.model.pywfile import PywFile
from pywriter.model.scene import Scene

SEPARATOR = '|'     # delimits data fields within a record.
LINEBREAK = '\t'    # substitutes embedded line breaks.


class SceneList(PywFile):
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
        Generate a csv file containing per scene:
        - manuscript scene hyperlink, 
        - scene title,
        - scene description.
        Return a message beginning with SUCCESS or ERROR.

    get_structure : None
        Return None to prevent structural comparison.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites PywFile._FILE_EXTENSION

    def read(self) -> str:
        """Read data from a csv file containing scene attributes. """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                table = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        for record in table:
            field = record.split(SEPARATOR)

            if 'ScID:' in field[0]:
                scId = re.search('ScID\:([0-9]+)', field[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].title = field[1]
                self.scenes[scId].desc = field[2].replace(LINEBREAK, '\n')
                #self.scenes[scId].wordCount = int(field[3])
                #self.scenes[scId].letterCount = int(field[4])
                self.scenes[scId].tags = field[5].split(';')

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
            ' ', '%20').replace('.csv', '_manuscript.odt')

        # first record: the table's column headings

        table = ['Scene link'
                 + SEPARATOR
                 + 'Scene title'
                 + SEPARATOR
                 + 'Scene description'
                 + SEPARATOR
                 + 'Word count'
                 + SEPARATOR
                 + 'Letter count'
                 + SEPARATOR
                 + 'Tags'
                 + '\n']

        # Add a record for each used scene in a regular chapter

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:

                        if self.scenes[scId].desc is not None:
                            sceneDesc = self.scenes[scId].desc.rstrip(
                            ).replace('\n', LINEBREAK)

                        else:
                            sceneDesc = ''

                        table.append('=HYPERLINK("file:///'
                                     + odtPath + '#ScID:' + scId + '";"ScID:' + scId + '")'
                                     + SEPARATOR
                                     + self.scenes[scId].title
                                     + SEPARATOR
                                     + sceneDesc
                                     + SEPARATOR
                                     + str(self.scenes[scId].wordCount)
                                     + SEPARATOR
                                     + str(self.scenes[scId].letterCount)
                                     + SEPARATOR
                                     + ';'.join(self.scenes[scId].tags)
                                     + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self) -> None:
        return None
