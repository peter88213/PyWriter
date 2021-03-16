"""CsvPlotList - Class for csv plot structure table.

Convention: 
* Used chapters marked "other" precede and describe plot sections (e.g. acts, steps).
* Tagged scenes contain plot events (e.g. inciting event, plot point, climax).
* Scene notes give plot relevant informations.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
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
        '''|$Tags|$Title|"$Notes"|''' +\
        '''$SceneNumber|$WordsTotal|$Field1|$Field2|$Field3|$Field4
'''

    def get_projectTemplateMapping(self):
        """Return a mapping dictionary for the project section. 
        """
        projectTemplateMapping = CsvFile.get_projectTemplateMapping(self)

        charList = []

        for crId in self.srtCharacters:
            charList.append(self.characters[crId].title)
            # Collect character names to identify storylines

        if self.fieldTitle1 in charList or self._STORYLINE_MARKER in self.fieldTitle1.lower():
            self.arc1 = True

        else:
            self.arc1 = False
            projectTemplateMapping['FieldTitle1'] = self._NOT_APPLICABLE

        if self.fieldTitle2 in charList or self._STORYLINE_MARKER in self.fieldTitle2.lower():
            self.arc2 = True

        else:
            self.arc2 = False
            projectTemplateMapping['FieldTitle2'] = self._NOT_APPLICABLE

        if self.fieldTitle3 in charList or self._STORYLINE_MARKER in self.fieldTitle3.lower():
            self.arc3 = True

        else:
            self.arc3 = False
            projectTemplateMapping['FieldTitle3'] = self._NOT_APPLICABLE

        if self.fieldTitle4 in charList or self._STORYLINE_MARKER in self.fieldTitle4.lower():
            self.arc4 = True

        else:
            self.arc4 = False
            projectTemplateMapping['FieldTitle4'] = self._NOT_APPLICABLE

        return projectTemplateMapping

    def get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section. 
        """
        sceneMapping = CsvFile.get_sceneMapping(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        if self.scenes[scId].field1 == '1' or not self.arc1:
            sceneMapping['Field1'] = ''

        if self.scenes[scId].field2 == '1' or not self.arc2:
            sceneMapping['Field2'] = ''

        if self.scenes[scId].field3 == '1' or not self.arc3:
            sceneMapping['Field3'] = ''

        if self.scenes[scId].field4 == '1' or not self.arc4:
            sceneMapping['Field4'] = ''

        return sceneMapping

    def read(self):
        """Parse the csv file located at filePath, fetching 
        the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        message = CsvFile.read(self)

        if message.startswith('ERROR'):
            return message

        tableHeader = self.rows[0]

        for cells in self.rows:

            if 'ChID:' in cells[0]:
                chId = re.search('ChID\:([0-9]+)', cells[0]).group(1)
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = cells[1]
                self.chapters[chId].desc = self.convert_to_yw(cells[4])

            if 'ScID:' in cells[0]:
                scId = re.search('ScID\:([0-9]+)', cells[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].tags = cells[2].split(self._LIST_SEPARATOR)
                self.scenes[scId].title = cells[3]
                self.scenes[scId].sceneNotes = self.convert_to_yw(cells[4])

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

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'
