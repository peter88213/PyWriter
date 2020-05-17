"""CsvSceneList - Class for csv scenes table.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.model.novel import Novel
from pywriter.model.scene import Scene

SCENELIST_SUFFIX = '_scenelist.csv'
MANUSCRIPT_SUFFIX = '_manuscript.odt'

SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
# '1' is assigned N/A (empty table cell).


class CsvSceneList(Novel):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites Novel._FILE_EXTENSION

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    _TABLE_HEADER = ('Scene link'
                     + _SEPARATOR
                     + 'Scene title'
                     + _SEPARATOR
                     + 'Scene description'
                     + _SEPARATOR
                     + 'Tags'
                     + _SEPARATOR
                     + 'Scene notes'
                     + _SEPARATOR
                     + 'Scene'
                     + _SEPARATOR
                     + 'Words total'
                     + _SEPARATOR
                     + 'Field 1'
                     + _SEPARATOR
                     + 'Field 2'
                     + _SEPARATOR
                     + 'Field 3'
                     + _SEPARATOR
                     + 'Field 4'
                     + _SEPARATOR
                     + 'Word count'
                     + _SEPARATOR
                     + 'Letter count'
                     + _SEPARATOR
                     + 'Status'
                     + '\n')

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                lines = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        cellsInLine = len(self._TABLE_HEADER.split(self._SEPARATOR))

        for line in lines:
            cell = line.rstrip().split(self._SEPARATOR)

            if len(cell) != cellsInLine:
                return 'ERROR: Wrong cell structure.'

            i = 0

            if 'ScID:' in cell[i]:
                scId = re.search('ScID\:([0-9]+)', cell[0]).group(1)
                self.scenes[scId] = Scene()
                i += 1
                self.scenes[scId].title = cell[i]
                i += 1
                self.scenes[scId].desc = cell[i].replace(
                    self._LINEBREAK, '\n')
                i += 1
                self.scenes[scId].tags = cell[i].split(';')
                i += 1
                self.scenes[scId].sceneNotes = cell[i].replace(
                    self._LINEBREAK, '\n')
                i += 1
                # Don't write back sceneCount
                i += 1
                # Don't write back wordCount
                i += 1

                # Transfer scene ratings; set to 1 if deleted

                if cell[i] in SCENE_RATINGS:
                    self.scenes[scId].field1 = cell[i]

                else:
                    self.scenes[scId].field1 = '1'

                i += 1

                if cell[i] in SCENE_RATINGS:
                    self.scenes[scId].field2 = cell[i]

                else:
                    self.scenes[scId].field2 = '1'

                i += 1

                if cell[i] in SCENE_RATINGS:
                    self.scenes[scId].field3 = cell[i]

                else:
                    self.scenes[scId].field3 = '1'

                i += 1

                if cell[i] in SCENE_RATINGS:
                    self.scenes[scId].field4 = cell[i]

                else:
                    self.scenes[scId].field4 = '1'

                i += 1
                # Don't write back scene words total
                i += 1
                # Don't write back scene letters total
                i += 1

                try:
                    self.scenes[scId].status = Scene.STATUS.index(cell[i])

                except ValueError:
                    pass
                    # Scene status remains None and will be ignored when
                    # writing back.

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def write(self, novel):
        """Generate a csv file containing per scene:
        - A manuscript scene hyperlink, 
        - scene title,
        - scene summary, 
        - scene word count, 
        - scene letter count,
        - scene tags.
        - scene notes.
        - scene fields.
        - scene status.
        Return a message beginning with SUCCESS or ERROR.
        """

        odtPath = os.path.realpath(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(SCENELIST_SUFFIX, MANUSCRIPT_SUFFIX)

        # Copy the scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        if novel.fieldTitle1 is not None:
            self.fieldTitle1 = novel.fieldTitle1

        else:
            self.fieldTitle1 = 'Field 1'

        if novel.fieldTitle2 is not None:
            self.fieldTitle2 = novel.fieldTitle2

        else:
            self.fieldTitle2 = 'Field 2'

        if novel.fieldTitle3 is not None:
            self.fieldTitle3 = novel.fieldTitle3

        else:
            self.fieldTitle3 = 'Field 3'

        if novel.fieldTitle4 is not None:
            self.fieldTitle4 = novel.fieldTitle4

        else:
            self.fieldTitle4 = 'Field 4'

        # first record: the table's column headings

        table = [self._TABLE_HEADER.replace(
            'Field 1', self.fieldTitle1).replace(
            'Field 2', self.fieldTitle2).replace(
            'Field 3', self.fieldTitle3).replace(
            'Field 4', self.fieldTitle4)]

        # Add a record for each used scene in a regular chapter

        sceneCount = 0
        wordCount = 0

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:
                        sceneCount += 1
                        wordCount += self.scenes[scId].wordCount

                        if self.scenes[scId].desc is None:
                            self.scenes[scId].desc = ''

                        if self.scenes[scId].tags is None:
                            self.scenes[scId].tags = ['']

                        if self.scenes[scId].sceneNotes is None:
                            self.scenes[scId].sceneNotes = ''

                        if self.scenes[scId].field1 is None:
                            self.scenes[scId].field1 = ''

                        if self.scenes[scId].field2 is None:
                            self.scenes[scId].field2 = ''

                        if self.scenes[scId].field3 is None:
                            self.scenes[scId].field3 = ''

                        if self.scenes[scId].field4 is None:
                            self.scenes[scId].field4 = ''

                        rating1 = ''
                        if self.scenes[scId].field1 != '1':
                            rating1 = self.scenes[scId].field1

                        rating2 = ''
                        if self.scenes[scId].field2 != '1':
                            rating2 = self.scenes[scId].field2

                        rating3 = ''
                        if self.scenes[scId].field3 != '1':
                            rating3 = self.scenes[scId].field3

                        rating4 = ''
                        if self.scenes[scId].field4 != '1':
                            rating4 = self.scenes[scId].field4

                        table.append('=HYPERLINK("file:///'
                                     + odtPath + '#ScID:' + scId + '%7Cregion";"ScID:' + scId + '")'
                                     + self._SEPARATOR
                                     + self.scenes[scId].title
                                     + self._SEPARATOR
                                     + self.scenes[scId].desc.rstrip().replace('\n', self._LINEBREAK)
                                     + self._SEPARATOR
                                     + ';'.join(self.scenes[scId].tags)
                                     + self._SEPARATOR
                                     + self.scenes[scId].sceneNotes.rstrip().replace('\n', self._LINEBREAK)
                                     + self._SEPARATOR
                                     + str(sceneCount)
                                     + self._SEPARATOR
                                     + str(wordCount)
                                     + self._SEPARATOR
                                     + rating1
                                     + self._SEPARATOR
                                     + rating2
                                     + self._SEPARATOR
                                     + rating3
                                     + self._SEPARATOR
                                     + rating4
                                     + self._SEPARATOR
                                     + str(self.scenes[scId].wordCount)
                                     + self._SEPARATOR
                                     + str(self.scenes[scId].letterCount)
                                     + self._SEPARATOR
                                     + Scene.STATUS[self.scenes[scId].status]
                                     + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self):
        """This file format has no comparable structure."""
        return None
