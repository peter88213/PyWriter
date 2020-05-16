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

STORYLINE_MARKER = 'story'
# Field names containing this string (case insensitive)
# are associated to storylines

SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
# '1' is assigned N/A (empty table cell).

NOT_APPLICABLE = 'N/A'
# Scene field column header for fields not being assigned to a storyline


class CsvPlotList(Novel):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites Novel._FILE_EXTENSION

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
                     + _SEPARATOR
                     + 'Scene'
                     + _SEPARATOR
                     + 'Word count'
                     + _SEPARATOR
                     + 'Field 1'
                     + _SEPARATOR
                     + 'Field 2'
                     + _SEPARATOR
                     + 'Field 3'
                     + _SEPARATOR
                     + 'Field 4'
                     + '\n')

    CHAR_STATE = ['', 'N/A', 'unhappy', 'dissatisfied',
                  'vague', 'satisfied', 'happy', '', '', '', '']

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

        cellsInLine = len(self._TABLE_HEADER.split(self._SEPARATOR))

        tableHeader = lines[0].rstrip().split(self._SEPARATOR)

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

                # Transfer scene ratings; set to 1 if deleted

                if cell[7] in SCENE_RATINGS:
                    self.scenes[scId].field1 = cell[7]

                elif tableHeader[7] != NOT_APPLICABLE:
                    self.scenes[scId].field1 = '1'

                if cell[8] in SCENE_RATINGS:
                    self.scenes[scId].field2 = cell[8]

                elif tableHeader[8] != NOT_APPLICABLE:
                    self.scenes[scId].field2 = '1'

                if cell[9] in SCENE_RATINGS:
                    self.scenes[scId].field3 = cell[9]

                elif tableHeader[9] != NOT_APPLICABLE:
                    self.scenes[scId].field3 = '1'

                if cell[10] in SCENE_RATINGS:
                    self.scenes[scId].field4 = cell[10]

                elif tableHeader[10] != NOT_APPLICABLE:
                    self.scenes[scId].field4 = '1'

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def write(self, novel):
        """Generate a csv file showing the novel's plot structure.
        Return a message beginning with SUCCESS or ERROR.
        """

        odtPath = os.path.realpath(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace(PLOTLIST_SUFFIX, MANUSCRIPT_SUFFIX)

        # Copy the chapter/scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        # first record: the table's column headings

        table = [self._TABLE_HEADER]

        # Identify storyline arcs

        charList = []

        for crId in novel.characters:
            charList.append(novel.characters[crId].title)

        if novel.fieldTitle1 in charList or STORYLINE_MARKER in novel.fieldTitle1.lower():
            table[0] = table[0].replace('Field 1', novel.fieldTitle1)
            arc1 = True

        else:
            table[0] = table[0].replace('Field 1', NOT_APPLICABLE)
            arc1 = False

        if novel.fieldTitle2 in charList or STORYLINE_MARKER in novel.fieldTitle2.lower():
            table[0] = table[0].replace('Field 2', novel.fieldTitle2)
            arc2 = True

        else:
            table[0] = table[0].replace('Field 2', NOT_APPLICABLE)
            arc2 = False

        if novel.fieldTitle3 in charList or STORYLINE_MARKER in novel.fieldTitle3.lower():
            table[0] = table[0].replace('Field 3', novel.fieldTitle3)
            arc3 = True

        else:
            table[0] = table[0].replace('Field 3', NOT_APPLICABLE)
            arc3 = False

        if novel.fieldTitle4 in charList or STORYLINE_MARKER in novel.fieldTitle4.lower():
            table[0] = table[0].replace('Field 4', novel.fieldTitle4)
            arc4 = True

        else:
            table[0] = table[0].replace('Field 4', NOT_APPLICABLE)
            arc4 = False

        # Add a record for each used scene in a regular chapter
        # and for each chapter marked "Other".

        sceneCount = 0
        wordCount = 0

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
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + self._SEPARATOR
                                 + '\n')

                else:
                    for scId in self.chapters[chId].srtScenes:

                        if not self.scenes[scId].isUnused:
                            sceneCount += 1
                            wordCount += self.scenes[scId].wordCount

                            # If the scene contains plot information:
                            # a tag marks the plot event (e.g. inciting event, plot point, climax).
                            # Put scene note text to "details".
                            # Transfer scene ratings > 1 to storyline arc
                            # states.

                            if self.scenes[scId].sceneNotes is None:
                                self.scenes[scId].sceneNotes = ''

                            if self.scenes[scId].tags is None:
                                self.scenes[scId].tags = ['']

                            arcState1 = ''
                            if arc1 and self.scenes[scId].field1 != '1':
                                arcState1 = self.scenes[scId].field1

                            arcState2 = ''
                            if arc2 and self.scenes[scId].field2 != '1':
                                arcState2 = self.scenes[scId].field2

                            arcState3 = ''
                            if arc3 and self.scenes[scId].field3 != '1':
                                arcState3 = self.scenes[scId].field3

                            arcState4 = ''
                            if arc4 and self.scenes[scId].field4 != '1':
                                arcState4 = self.scenes[scId].field4

                            table.append('=HYPERLINK("file:///'
                                         + odtPath + '#ScID:' + scId + '%7Cregion";"ScID:' + scId + '")'
                                         + self._SEPARATOR
                                         + self._SEPARATOR
                                         + ';'.join(self.scenes[scId].tags)
                                         + self._SEPARATOR
                                         + self.scenes[scId].title
                                         + self._SEPARATOR
                                         + self.scenes[scId].sceneNotes.rstrip().replace('\n', self._LINEBREAK)
                                         + self._SEPARATOR
                                         + str(sceneCount)
                                         + self._SEPARATOR
                                         + str(wordCount)
                                         + self._SEPARATOR
                                         + arcState1
                                         + self._SEPARATOR
                                         + arcState2
                                         + self._SEPARATOR
                                         + arcState3
                                         + self._SEPARATOR
                                         + arcState4
                                         + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self):
        return None
