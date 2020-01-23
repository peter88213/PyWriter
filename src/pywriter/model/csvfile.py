"""CsvFile - Class for csv scenes table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
from pywriter.model.pywfile import PywFile
from pywriter.model.scene import Scene

SEPARATOR = '|'
LINEBREAK = '\t'


class CsvFile(PywFile):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a row per scene.

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
    """

    _fileExtension = 'csv'
    # overwrites PywFile._fileExtension

    def read(self):
        """Read data from a csv file containing scene attributes. """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                table = (f.readlines())

        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        for row in table:
            cell = row.split(SEPARATOR)

            if 'ScID:' in cell[0]:
                scId = re.search('ScID\:([0-9]+)', cell[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].title = cell[1]
                self.scenes[scId].desc = cell[2].replace(LINEBREAK, '\n')
                #self.scenes[scId].wordCount = int(cell[3])
                #self.scenes[scId].letterCount = int(cell[4])

        return('SUCCESS: Data read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write scene attributes to csv file. """

        # Copy the scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        odtPath = (os.getcwd().replace('\\', '/') + '/' +
                   self.filePath).replace(' ', '%20').replace('.csv', '_manuscript.odt')

        # First row: column headings

        table = ['Scene link'
                 + SEPARATOR
                 + 'Scene title'
                 + SEPARATOR
                 + 'Scene description'
                 + SEPARATOR
                 + 'Word count'
                 + SEPARATOR
                 + 'Letter count'
                 + '\n']

        for chId in self.srtChapters:

            for scId in self.chapters[chId].srtScenes:

                # Add a row for each scene

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
                             + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
