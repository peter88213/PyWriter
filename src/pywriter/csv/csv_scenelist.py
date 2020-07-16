"""CsvSceneList - Class for csv scenes table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.csv.csv_file import CsvFile
from pywriter.model.scene import Scene


class CsvSceneList(CsvFile):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the _SEPARATOR character.
    """

    SUFFIX = '_scenelist'

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    fileHeader = '''Scene link|''' +\
        '''Scene title|Scene description|Tags|Scene notes|''' +\
        '''A/R|Goal|Conflict|Outcome|''' +\
        '''Scene|Words total|$FieldTitle1|$FieldTitle2|$FieldTitle3|$FieldTitle4|''' +\
        '''Word count|Letter count|Status|''' +\
        '''Characters|Locations|Items
'''

    sceneTemplate = '''=HYPERLINK("file:///$ProjectPath/${ProjectName}_manuscript.odt#ScID:$ID%7Cregion";"ScID:$ID")|''' +\
        '''$Title|$Desc|$Tags|$Notes|''' +\
        '''$ReactionScene|$Goal|$Conflict|$Outcome|''' +\
        '''$SceneNumber|$WordsTotal|$Field1|$Field2|$Field3|$Field4|''' +\
        '''$WordCount|$LetterCount|$Status|''' +\
        '''$Characters|$Locations|$Items
'''

    def get_sceneSubst(self, scId, sceneNumber, wordsTotal, lettersTotal):
        sceneSubst = CsvFile.get_sceneSubst(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        if self.scenes[scId].field1 == '1':
            sceneSubst['Field1'] = ''

        if self.scenes[scId].field2 == '1':
            sceneSubst['Field2'] = ''

        if self.scenes[scId].field3 == '1':
            sceneSubst['Field3'] = ''

        if self.scenes[scId].field4 == '1':
            sceneSubst['Field4'] = ''

        return sceneSubst

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

        cellsInLine = len(self.fileHeader.split(self._SEPARATOR))

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
                self.scenes[scId].tags = cell[i].split(self._LIST_SEPARATOR)
                i += 1
                self.scenes[scId].sceneNotes = cell[i].replace(
                    self._LINEBREAK, '\n')
                i += 1

                if Scene.REACTION_MARKER.lower() in cell[i].lower():
                    self.scenes[scId].isReactionScene = True

                else:
                    self.scenes[scId].isReactionScene = False

                i += 1
                self.scenes[scId].goal = cell[i].replace(
                    self._LINEBREAK, ' ')
                i += 1
                self.scenes[scId].conflict = cell[i].replace(
                    self._LINEBREAK, ' ')
                i += 1
                self.scenes[scId].outcome = cell[i].replace(
                    self._LINEBREAK, ' ')
                i += 1
                # Don't write back sceneCount
                i += 1
                # Don't write back wordCount
                i += 1

                # Transfer scene ratings; set to 1 if deleted

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field1 = cell[i]

                else:
                    self.scenes[scId].field1 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field2 = cell[i]

                else:
                    self.scenes[scId].field2 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field3 = cell[i]

                else:
                    self.scenes[scId].field3 = '1'

                i += 1

                if cell[i] in self._SCENE_RATINGS:
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

                i += 1
                ''' Cannot write back character IDs, because self.characters is None
                charaNames = cell[i].split(self._LIST_SEPARATOR)
                self.scenes[scId].characters = []

                for charaName in charaNames:

                    for id, name in self.characters.items():

                        if name == charaName:
                            self.scenes[scId].characters.append(id)
                '''
                i += 1
                ''' Cannot write back location IDs, because self.locations is None
                locaNames = cell[i].split(self._LIST_SEPARATOR)
                self.scenes[scId].locations = []

                for locaName in locaNames:

                    for id, name in self.locations.items():

                        if name == locaName:
                            self.scenes[scId].locations.append(id)
                '''
                i += 1
                ''' Cannot write back item IDs, because self.items is None
                itemNames = cell[i].split(self._LIST_SEPARATOR)
                self.scenes[scId].items = []

                for itemName in itemNames:

                    for id, name in self.items.items():

                        if name == itemName:
                            self.scenes[scId].items.append(id)
                '''

        return 'SUCCESS: Data read from "' + self._filePath + '".'
