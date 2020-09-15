"""CsvPlotList - Class for csv plot structure table.

Convention: 
* Used chapters marked "other" precede and describe plot sections (e.g. acts, steps).
* Tagged scenes contain plot events (e.g. inciting event, plot point, climax).
* Scene notes give plot relevant informations.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class CsvPlotList(CsvFile):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    DESCRIPTION = 'Plot list'
    SUFFIX = '_plotlist'

    _SEPARATOR = '|'     # delimits data fields within a record.
    _LINEBREAK = '\t'    # substitutes embedded line breaks.

    _STORYLINE_MARKER = 'story'
    # Field names containing this string (case insensitive)
    # are associated to storylines

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    _NOT_APPLICABLE = 'N/A'
    # Scene field column header for fields not being assigned to a storyline

    _CHAR_STATE = ['', 'N/A', 'unhappy', 'dissatisfied',
                   'vague', 'satisfied', 'happy', '', '', '', '']

    fileHeader = '''ID|''' +\
        '''Plot section|Plot event|Plot event title|Details|''' +\
        '''Scene|Words total|$FieldTitle1|$FieldTitle2|$FieldTitle3|$FieldTitle4
'''

    notesChapterTemplate = '''ChID:$ID|$Title|||$Desc||||||
'''

    sceneTemplate = '''=HYPERLINK("file:///$ProjectPath/${ProjectName}_manuscript.odt#ScID:$ID%7Cregion";"ScID:$ID")|''' +\
        '''|$Tags|$Title|$Notes|''' +\
        '''$SceneNumber|$WordsTotal|$Field1|$Field2|$Field3|$Field4
'''

    def get_projectTemplateSubst(self):
        projectTemplateSubst = CsvFile.get_projectTemplateSubst(self)

        charList = []

        for crId in self.characters:
            charList.append(self.characters[crId].title)

        if self.fieldTitle1 in charList or self._STORYLINE_MARKER in self.fieldTitle1.lower():
            self.arc1 = True

        else:
            self.arc1 = False
            projectTemplateSubst['FieldTitle1'] = self._NOT_APPLICABLE

        if self.fieldTitle2 in charList or self._STORYLINE_MARKER in self.fieldTitle2.lower():
            self.arc2 = True

        else:
            self.arc2 = False
            projectTemplateSubst['FieldTitle2'] = self._NOT_APPLICABLE

        if self.fieldTitle3 in charList or self._STORYLINE_MARKER in self.fieldTitle3.lower():
            self.arc3 = True

        else:
            self.arc3 = False
            projectTemplateSubst['FieldTitle3'] = self._NOT_APPLICABLE

        if self.fieldTitle4 in charList or self._STORYLINE_MARKER in self.fieldTitle4.lower():
            self.arc4 = True

        else:
            self.arc4 = False
            projectTemplateSubst['FieldTitle4'] = self._NOT_APPLICABLE

        return projectTemplateSubst

    def get_sceneSubst(self, scId, sceneNumber, wordsTotal, lettersTotal):
        sceneSubst = CsvFile.get_sceneSubst(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        if self.scenes[scId].field1 == '1' or not self.arc1:
            sceneSubst['Field1'] = ''

        if self.scenes[scId].field2 == '1' or not self.arc1:
            sceneSubst['Field2'] = ''

        if self.scenes[scId].field3 == '1' or not self.arc3:
            sceneSubst['Field3'] = ''

        if self.scenes[scId].field4 == '1' or not self.arc4:
            sceneSubst['Field4'] = ''

        return sceneSubst

    def read(self):
        """Parse the csv file located at filePath, fetching 
        the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                lines = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self._filePath) + '" not found.'

        cellsInLine = len(self.fileHeader.split(self._SEPARATOR))

        tableHeader = lines[0].rstrip().split(self._SEPARATOR)

        for line in lines:
            cell = line.rstrip().split(self._SEPARATOR)

            if len(cell) != cellsInLine:
                return 'ERROR: Wrong cell structure.'

            if 'ChID:' in cell[0]:
                chId = re.search('ChID\:([0-9]+)', cell[0]).group(1)
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = cell[1]
                self.chapters[chId].desc = self.convert_to_yw(cell[4])

            if 'ScID:' in cell[0]:
                scId = re.search('ScID\:([0-9]+)', cell[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].tags = cell[2].split(self._LIST_SEPARATOR)
                self.scenes[scId].title = cell[3]
                self.scenes[scId].sceneNotes = self.convert_to_yw(cell[4])

                i = 5
                # Don't write back sceneCount
                i += 1
                # Don't write back wordCount
                i += 1

                # Transfer scene ratings; set to 1 if deleted

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field1 = cell[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field1 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field2 = cell[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field2 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field3 = cell[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field3 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field4 = cell[i]

                elif tableHeader[i] != self._NOT_APPLICABLE:
                    self.scenes[scId].field4 = '1'

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def get_structure(self):
        """returns a string showing the order of scenes.
        """
        lines = []

        for scId in self.scenes:
            lines.append('  ScID:' + str(scId))

        return '\n'.join(lines)
