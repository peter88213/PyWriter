"""Manuscript - Class for csv scene list file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
from pywriter.model.pywfile import PywFile
from pywriter.model.scene import Scene

MD_HEADING_MARKERS = ("##", "#")
# Index is yWriter's chapter type:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


SEPARATOR = '|'


class CsvFile(PywFile):
    """csv file representation of an yWriter project's scene list. 

    Represents a csv file with a selection of scene attributes.

    # Attributes

    _text : str
        contains the parsed data.

    _collectText : bool
        simple parsing state indicator. 
        True means: the data returned by the html parser 
        belongs to the body section. 

    # Methods

    read : str
        parse the Markdown file located at filePath, fetching 
        the Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Generate a Markdown file containing:
        - chapter ID tags,
        - chapter headings,
        - scene ID tags, 
        - scene content.
        Return a message beginning with SUCCESS or ERROR.
    """

    _fileExtension = 'csv'
    # overwrites PywFile._fileExtension

    def read(self):
        """Read data from a csv file containing scene attributes. """

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                csvData = (f.readlines())

        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        for line in csvData:

            attributes = line.split(SEPARATOR)

            if 'ScID:' in attributes[0]:
                scId = re.search('ScID\:([0-9]+)', attributes[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].title = attributes[1]
                self.scenes[scId].desc = attributes[2].replace(' && ', '\n')

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
        csvData = ['Scene link' + SEPARATOR +
                   'Scene title' + SEPARATOR + 'Scene description\n']

        for chId in self.srtChapters:

            for scId in self.chapters[chId].srtScenes:
                sceneTitle = self.scenes[scId].title.rstrip()

                if self.scenes[scId].desc is not None:
                    sceneDesc = self.scenes[scId].desc.rstrip(
                    ).replace('\n', ' && ')

                else:
                    sceneDesc = ''

                csvData.append('=HYPERLINK("file:///'
                               + odtPath + '#ScID:' + scId + '";"ScID:' + scId + '")'
                               + SEPARATOR
                               + sceneTitle
                               + SEPARATOR
                               + sceneDesc
                               + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(csvData)

        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')
