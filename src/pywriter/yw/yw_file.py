"""yWFile - Class for yWriter xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.object import Object
from pywriter.yw.yw_form import *


class YwFile(Novel):
    """yWriter xml project file representation."""

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']
        # Names of yWriter xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """

        if filePath.lower().endswith('.yw7'):
            self._FILE_EXTENSION = '.yw7'
            self._ENCODING = 'utf-8'
            self._filePath = filePath

        if filePath.lower().endswith('.yw6'):
            self._FILE_EXTENSION = '.yw6'
            self._ENCODING = 'utf-8'
            self._filePath = filePath

        elif filePath.lower().endswith('.yw5'):
            self._FILE_EXTENSION = '.yw5'
            self._ENCODING = 'iso-8859-1'
            self._filePath = filePath

    def read(self):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        def readProjectLevel():
            prj = root.find('PROJECT')
            self.title = prj.find('Title').text

            if prj.find('AuthorName') is not None:
                self.author = prj.find('AuthorName').text

            if prj.find('Desc') is not None:
                self.desc = prj.find('Desc').text

            self.fieldTitle1 = prj.find('FieldTitle1').text
            self.fieldTitle2 = prj.find('FieldTitle2').text
            self.fieldTitle3 = prj.find('FieldTitle3').text
            self.fieldTitle4 = prj.find('FieldTitle4').text

        def readChapterLevel():

            for chp in root.iter('CHAPTER'):
                chId = chp.find('ID').text
                self.chapters[chId] = Chapter()
                self.chapters[chId].title = chp.find('Title').text
                self.srtChapters.append(chId)

                if chp.find('Desc') is not None:
                    self.chapters[chId].desc = chp.find('Desc').text

                if chp.find('SectionStart') is not None:
                    self.chapters[chId].chLevel = 1

                else:
                    self.chapters[chId].chLevel = 0

                self.chapters[chId].chType = int(chp.find('Type').text)

                if chp.find('Unused') is not None:
                    self.chapters[chId].isUnused = True

                else:
                    self.chapters[chId].isUnused = False

                for fields in chp.findall('Fields'):

                    if fields.find('Field_SuppressChapterTitle') is not None:

                        if fields.find('Field_SuppressChapterTitle').text == '1':
                            self.chapters[chId].suppressChapterTitle = True

                        else:
                            self.chapters[chId].suppressChapterTitle = False

                self.chapters[chId].srtScenes = []

                if chp.find('Scenes') is not None:

                    for scn in chp.find('Scenes').findall('ScID'):
                        scId = scn.text
                        self.chapters[chId].srtScenes.append(scId)

        def readSceneLevel():

            for scn in root.iter('SCENE'):
                scId = scn.find('ID').text

                self.scenes[scId] = Scene()
                self.scenes[scId].title = scn.find('Title').text

                if scn.find('Desc') is not None:
                    self.scenes[scId].desc = scn.find('Desc').text

                if scn.find('SceneContent') is not None:
                    sceneContent = scn.find('SceneContent').text

                    if sceneContent is not None:
                        self.scenes[scId].sceneContent = sceneContent

                if scn.find('Unused') is not None:
                    self.scenes[scId].isUnused = True

                else:
                    self.scenes[scId].isUnused = False

                if scn.find('Status') is not None:
                    self.scenes[scId].status = int(scn.find('Status').text)

                if scn.find('Notes') is not None:
                    self.scenes[scId].sceneNotes = scn.find('Notes').text

                if scn.find('Tags') is not None:

                    if scn.find('Tags').text is not None:
                        self.scenes[scId].tags = scn.find(
                            'Tags').text.split(';')

                if scn.find('Field1') is not None:
                    self.scenes[scId].field1 = scn.find('Field1').text

                if scn.find('Field2') is not None:
                    self.scenes[scId].field2 = scn.find('Field2').text

                if scn.find('Field3') is not None:
                    self.scenes[scId].field3 = scn.find('Field3').text

                if scn.find('Field4') is not None:
                    self.scenes[scId].field4 = scn.find('Field4').text

                if scn.find('AppendToPrev') is not None:
                    self.scenes[scId].appendToPrev = True

                else:
                    self.scenes[scId].appendToPrev = False

                if scn.find('ReactionScene') is not None:
                    self.scenes[scId].isReactionScene = True

                else:
                    self.scenes[scId].isReactionScene = False

                if scn.find('Goal') is not None:
                    self.scenes[scId].goal = scn.find('Goal').text

                if scn.find('Conflict') is not None:
                    self.scenes[scId].conflict = scn.find('Conflict').text

                if scn.find('Outcome') is not None:
                    self.scenes[scId].outcome = scn.find('Outcome').text

                for crId in scn.find('Characters').iter('CharID'):

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    self.scenes[scId].characters.append(crId.text)

                for lcId in scn.find('Locations').iter('LocID'):

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    self.scenes[scId].locations.append(lcId.text)

                for itId in scn.find('Items').iter('ItemID'):

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    self.scenes[scId].items.append(itId.text)

        def readCharacters():

            for crt in root.iter('CHARACTER'):
                crId = crt.find('ID').text

                self.characters[crId] = Character()
                self.characters[crId].title = crt.find('Title').text

                if crt.find('Desc') is not None:
                    self.characters[crId].desc = crt.find('Desc').text

                if crt.find('AKA') is not None:
                    self.characters[crId].aka = crt.find('AKA').text

                if crt.find('Tags') is not None:

                    if crt.find('Tags').text is not None:
                        self.characters[crId].tags = crt.find(
                            'Tags').text.split(';')

                if crt.find('Notes') is not None:
                    self.characters[crId].notes = crt.find('Notes').text

                if crt.find('Bio') is not None:
                    self.characters[crId].bio = crt.find('Bio').text

                if crt.find('Goals') is not None:
                    self.characters[crId].goals = crt.find('Goals').text

                if crt.find('FullName') is not None:
                    self.characters[crId].fullName = crt.find('FullName').text

                if crt.find('Major') is not None:
                    self.characters[crId].isMajor = True

                else:
                    self.characters[crId].isMajor = False

        def readLocations():

            for loc in root.iter('LOCATION'):
                lcId = loc.find('ID').text

                self.locations[lcId] = Object()
                self.locations[lcId].title = loc.find('Title').text

                if loc.find('Desc') is not None:
                    self.locations[lcId].desc = loc.find('Desc').text

                if loc.find('AKA') is not None:
                    self.locations[lcId].aka = loc.find('AKA').text

                if loc.find('Tags') is not None:

                    if loc.find('Tags').text is not None:
                        self.locations[lcId].tags = loc.find(
                            'Tags').text.split(';')

        def readItems():

            for itm in root.iter('ITEM'):
                itId = itm.find('ID').text

                self.items[itId] = Object()
                self.items[itId].title = itm.find('Title').text

                if itm.find('Desc') is not None:
                    self.items[itId].desc = itm.find('Desc').text

                if itm.find('AKA') is not None:
                    self.items[itId].aka = itm.find('AKA').text

                if itm.find('Tags') is not None:

                    if itm.find('Tags').text is not None:
                        self.items[itId].tags = itm.find(
                            'Tags').text.split(';')

        # Complete list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r', encoding=self._ENCODING) as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)

            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        # Open the file again in order let ElementTree parse its xml structure.

        try:
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        # Retrieve the XML element tree items.

        readCharacters()
        readLocations()
        readItems()
        readProjectLevel()
        readChapterLevel()
        readSceneLevel()

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel):
        """Open the yWriter xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        def copyProjectLevel():

            if novel.title:
                # avoids deleting the title, if it is empty by accident
                self.title = novel.title

            if novel.desc is not None:
                self.desc = novel.desc

            if novel.author is not None:
                self.author = novel.author

            if novel.fieldTitle1 is not None:
                self.fieldTitle1 = novel.fieldTitle1

            if novel.fieldTitle2 is not None:
                self.fieldTitle2 = novel.fieldTitle2

            if novel.fieldTitle3 is not None:
                self.fieldTitle3 = novel.fieldTitle3

            if novel.fieldTitle4 is not None:
                self.fieldTitle4 = novel.fieldTitle4

            '''Do not modify these items yet:
            
            if novel.srtChapters != []:
                self.srtChapters = novel.srtChapters
                
            '''

        def writeProjectLevel():
            prj = root.find('PROJECT')
            prj.find('Title').text = self.title
            prj.find('FieldTitle1').text = self.fieldTitle1
            prj.find('FieldTitle2').text = self.fieldTitle2
            prj.find('FieldTitle3').text = self.fieldTitle3
            prj.find('FieldTitle4').text = self.fieldTitle4

            if self.desc is not None:

                if prj.find('Desc') is None:
                    newDesc = ET.SubElement(prj, 'Desc')
                    newDesc.text = self.desc

                else:
                    prj.find('Desc').text = self.desc

            if self.author is not None:

                if prj.find('AuthorName') is None:
                    newAuth = ET.SubElement(prj, 'AuthorName')
                    newAuth.text = self.author

                else:
                    prj.find('AuthorName').text = self.author

        def copyChapterLevel():

            if novel.chapters != {}:

                for chId in novel.chapters:

                    if novel.chapters[chId].title:
                        # avoids deleting the title, if it is empty by accident
                        self.chapters[chId].title = novel.chapters[chId].title

                    if novel.chapters[chId].desc is not None:
                        self.chapters[chId].desc = novel.chapters[chId].desc

                    if novel.chapters[chId].chLevel is not None:
                        self.chapters[chId].chLevel = novel.chapters[chId].chLevel

                    if novel.chapters[chId].chType is not None:
                        self.chapters[chId].chType = novel.chapters[chId].chType

                    if novel.chapters[chId].isUnused is not None:
                        self.chapters[chId].isUnused = novel.chapters[chId].isUnused

                    if novel.chapters[chId].suppressChapterTitle is not None:
                        self.chapters[chId].suppressChapterTitle = novel.chapters[chId].suppressChapterTitle

                    '''Do not modify these items yet:
                    
                    if novel.chapters[chId].srtScenes != []:
                        self.chapters[chId].srtScenes = novel.chapters[chId].srtScenes

                    '''

        def writeChapterLevel():

            for chp in root.iter('CHAPTER'):
                chId = chp.find('ID').text

                if chId in self.chapters:
                    chp.find('Title').text = self.chapters[chId].title

                    if self.chapters[chId].desc is not None:

                        if chp.find('Desc') is None:
                            newDesc = ET.SubElement(chp, 'Desc')
                            newDesc.text = self.chapters[chId].desc

                        else:
                            chp.find('Desc').text = self.chapters[chId].desc

                    levelInfo = chp.find('SectionStart')

                    if levelInfo is not None:

                        if self.chapters[chId].chLevel == 0:
                            chp.remove(levelInfo)

                    chp.find('Type').text = str(self.chapters[chId].chType)

                    if self.chapters[chId].isUnused:

                        if chp.find('Unused') is None:
                            newUnused = ET.SubElement(chp, 'Unused')
                            newUnused.text = '-1'

                    elif chp.find('Unused') is not None:
                        chp.remove(chp.find('Unused'))

        def copySceneLevel():
            sceneCount = 0

            if novel.scenes != {}:

                for scId in novel.scenes:

                    if novel.scenes[scId].title:
                        # avoids deleting the title, if it is empty by accident
                        self.scenes[scId].title = novel.scenes[scId].title

                    if novel.scenes[scId].desc is not None:
                        self.scenes[scId].desc = novel.scenes[scId].desc

                    if novel.scenes[scId].sceneContent is not None:
                        self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent
                        sceneCount += 1

                    if novel.scenes[scId].isUnused is not None:
                        self.scenes[scId].isUnused = novel.scenes[scId].isUnused

                    if novel.scenes[scId].status is not None:
                        self.scenes[scId].status = novel.scenes[scId].status

                    if novel.scenes[scId].sceneNotes is not None:
                        self.scenes[scId].sceneNotes = novel.scenes[scId].sceneNotes

                    if novel.scenes[scId].tags is not None:
                        self.scenes[scId].tags = novel.scenes[scId].tags

                    if novel.scenes[scId].field1 is not None:
                        self.scenes[scId].field1 = novel.scenes[scId].field1

                    if novel.scenes[scId].field2 is not None:
                        self.scenes[scId].field2 = novel.scenes[scId].field2

                    if novel.scenes[scId].field3 is not None:
                        self.scenes[scId].field3 = novel.scenes[scId].field3

                    if novel.scenes[scId].field4 is not None:
                        self.scenes[scId].field4 = novel.scenes[scId].field4

                    if novel.scenes[scId].appendToPrev is not None:
                        self.scenes[scId].appendToPrev = novel.scenes[scId].appendToPrev

                    if novel.scenes[scId].isReactionScene is not None:
                        self.scenes[scId].isReactionScene = novel.scenes[scId].isReactionScene

                    if novel.scenes[scId].goal is not None:
                        self.scenes[scId].goal = novel.scenes[scId].goal

                    if novel.scenes[scId].conflict is not None:
                        self.scenes[scId].conflict = novel.scenes[scId].conflict

                    if novel.scenes[scId].outcome is not None:
                        self.scenes[scId].outcome = novel.scenes[scId].outcome

                    if novel.scenes[scId].characters is not None:
                        self.scenes[scId].characters = []

                        for crId in novel.scenes[scId].characters:

                            if crId in self.characters:
                                self.scenes[scId].characters.append(crId)

                    if novel.scenes[scId].locations is not None:
                        self.scenes[scId].locations = []

                        for lcId in novel.scenes[scId].locations:

                            if lcId in self.locations:
                                self.scenes[scId].locations.append(lcId)

                    if novel.scenes[scId].items is not None:
                        self.scenes[scId].items = []

                        for itId in novel.scenes[scId].items:

                            if itId in self.items:
                                self.scenes[scId].append(crId)

                return sceneCount

        def writeSceneLevel():

            for scn in root.iter('SCENE'):
                scId = scn.find('ID').text

                if scId in self.scenes:

                    if self.scenes[scId].title is not None:
                        scn.find('Title').text = self.scenes[scId].title

                    if self.scenes[scId].desc is not None:

                        if scn.find('Desc') is None:
                            newDesc = ET.SubElement(scn, 'Desc')
                            newDesc.text = self.scenes[scId].desc

                        else:
                            scn.find('Desc').text = self.scenes[scId].desc

                    if self.scenes[scId]._sceneContent is not None:
                        scn.find(
                            'SceneContent').text = self.scenes[scId]._sceneContent
                        scn.find('WordCount').text = str(
                            self.scenes[scId].wordCount)
                        scn.find('LetterCount').text = str(
                            self.scenes[scId].letterCount)

                    if self.scenes[scId].isUnused:

                        if scn.find('Unused') is None:
                            newUnused = ET.SubElement(scn, 'Unused')
                            newUnused.text = '-1'

                    elif scn.find('Unused') is not None:
                        scn.remove(scn.find('Unused'))

                    if self.scenes[scId].status is not None:
                        scn.find('Status').text = str(self.scenes[scId].status)

                    if self.scenes[scId].sceneNotes is not None:

                        if scn.find('Notes') is None:
                            newNotes = ET.SubElement(scn, 'Notes')
                            newNotes.text = self.scenes[scId].sceneNotes

                        else:
                            scn.find(
                                'Notes').text = self.scenes[scId].sceneNotes

                    if self.scenes[scId].tags is not None:

                        if scn.find('Tags') is None:
                            newTags = ET.SubElement(scn, 'Tags')
                            newTags.text = ';'.join(self.scenes[scId].tags)

                        else:
                            scn.find('Tags').text = ';'.join(
                                self.scenes[scId].tags)

                    if self.scenes[scId].field1 is not None:

                        if scn.find('Field1') is None:
                            newField = ET.SubElement(scn, 'Field1')
                            newField.text = self.scenes[scId].field1

                        else:
                            scn.find('Field1').text = self.scenes[scId].field1

                    if self.scenes[scId].field2 is not None:

                        if scn.find('Field2') is None:
                            newField = ET.SubElement(scn, 'Field2')
                            newField.text = self.scenes[scId].field2

                        else:
                            scn.find('Field2').text = self.scenes[scId].field2

                    if self.scenes[scId].field3 is not None:

                        if scn.find('Field3') is None:
                            newField = ET.SubElement(scn, 'Field3')
                            newField.text = self.scenes[scId].field3

                        else:
                            scn.find('Field3').text = self.scenes[scId].field3

                    if self.scenes[scId].field4 is not None:

                        if scn.find('Field4') is None:
                            newField = ET.SubElement(scn, 'Field4')
                            newField.text = self.scenes[scId].field4

                        else:
                            scn.find('Field4').text = self.scenes[scId].field4

                    if self.scenes[scId].appendToPrev:

                        if scn.find('AppendToPrev') is None:
                            newAppendToPrev = ET.SubElement(
                                scn, 'AppendToPrev')
                            newAppendToPrev.text = '-1'

                    elif scn.find('AppendToPrev') is not None:
                        scn.remove(scn.find('AppendToPrev'))

                    if self.scenes[scId].isReactionScene:

                        if scn.find('ReactionScene') is None:
                            newReactionScene = ET.SubElement(
                                scn, 'ReactionScene')
                            newReactionScene.text = '-1'

                    elif scn.find('ReactionScene') is not None:
                        scn.remove(scn.find('ReactionScene'))

                    if self.scenes[scId].goal is not None:

                        if scn.find('Goal') is None:
                            newGoal = ET.SubElement(scn, 'Goal')
                            newGoal.text = self.scenes[scId].goal

                        else:
                            scn.find('Goal').text = self.scenes[scId].goal

                    if self.scenes[scId].conflict is not None:

                        if scn.find('Conflict') is None:
                            newConflict = ET.SubElement(scn, 'Conflict')
                            newConflict.text = self.scenes[scId].conflict

                        else:
                            scn.find(
                                'Conflict').text = self.scenes[scId].conflict

                    if self.scenes[scId].outcome is not None:

                        if scn.find('Outcome') is None:
                            newOutcome = ET.SubElement(scn, 'Outcome')
                            newOutcome.text = self.scenes[scId].outcome

                        else:
                            scn.find(
                                'Outcome').text = self.scenes[scId].outcome

                    if self.scenes[scId].characters is not None:
                        characters = scn.find('Characters')

                        for oldCrId in characters.findall('CharID'):
                            characters.remove(oldCrId)

                        for crId in self.scenes[scId].characters:
                            newCrId = ET.SubElement(characters, 'CharID')
                            newCrId.text = crId

                    if self.scenes[scId].locations is not None:
                        locations = scn.find('Locations')

                        for oldLcId in locations.findall('LocID'):
                            locations.remove(oldLcId)

                        for lcId in self.scenes[scId].locations:
                            newLcId = ET.SubElement(locations, 'LocID')
                            newLcId.text = lcId

                    if self.scenes[scId].items is not None:
                        items = scn.find('Items')

                        for oldItId in items.findall('ItemID'):
                            items.remove(oldItId)

                        for itId in self.scenes[scId].items:
                            newItId = ET.SubElement(items, 'ItemID')
                            newItId.text = itId

        def copyCharacters():

            if novel.characters != {}:

                for crId in novel.characters:

                    if novel.characters[crId].title:
                        # avoids deleting the title, if it is empty by accident
                        self.characters[crId].title = novel.characters[crId].title

                    if novel.characters[crId].desc is not None:
                        self.characters[crId].desc = novel.characters[crId].desc

                    if novel.characters[crId].aka is not None:
                        self.characters[crId].aka = novel.characters[crId].aka

                    if novel.characters[crId].tags is not None:
                        self.characters[crId].tags = novel.characters[crId].tags

                    if novel.characters[crId].notes is not None:
                        self.characters[crId].notes = novel.characters[crId].notes

                    if novel.characters[crId].bio is not None:
                        self.characters[crId].bio = novel.characters[crId].bio

                    if novel.characters[crId].goals is not None:
                        self.characters[crId].goals = novel.characters[crId].goals

                    if novel.characters[crId].fullName is not None:
                        self.characters[crId].fullName = novel.characters[crId].fullName

                    if novel.characters[crId].isMajor is not None:
                        self.characters[crId].isMajor = novel.characters[crId].isMajor

        def writeCharacters():

            for crt in root.iter('CHARACTER'):
                crId = crt.find('ID').text

                if crId in self.characters:

                    if self.characters[crId].title is not None:
                        crt.find('Title').text = self.characters[crId].title

                    if self.characters[crId].desc is not None:

                        if crt.find('Desc') is None:
                            newDesc = ET.SubElement(crt, 'Desc')
                            newDesc.text = self.characters[crId].desc

                        else:
                            crt.find('Desc').text = self.characters[crId].desc

                    if self.characters[crId].aka is not None:

                        if crt.find('AKA') is None:
                            newAka = ET.SubElement(crt, 'AKA')
                            newAka.text = self.characters[crId].aka

                        else:
                            crt.find('AKA').text = self.characters[crId].aka

                    if self.characters[crId].tags is not None:

                        if crt.find('Tags') is None:
                            newTags = ET.SubElement(crt, 'Tags')
                            newTags.text = ';'.join(self.characters[crId].tags)

                        else:
                            crt.find('Tags').text = ';'.join(
                                self.characters[crId].tags)

                    if self.characters[crId].notes is not None:

                        if crt.find('Notes') is None:
                            newNotes = ET.SubElement(crt, 'Notes')
                            newNotes.text = self.characters[crId].notes

                        else:
                            crt.find(
                                'Notes').text = self.characters[crId].notes

                    if self.characters[crId].bio is not None:

                        if crt.find('Bio') is None:
                            newBio = ET.SubElement(crt, 'Bio')
                            newBio.text = self.characters[crId].bio

                        else:
                            crt.find('Bio').text = self.characters[crId].bio

                    if self.characters[crId].goals is not None:

                        if crt.find('Goals') is None:
                            newGoals = ET.SubElement(crt, 'Goals')
                            newGoals.text = self.characters[crId].goals

                        else:
                            crt.find(
                                'Goals').text = self.characters[crId].goals

                    if self.characters[crId].fullName is not None:

                        if crt.find('FullName') is None:
                            newFullName = ET.SubElement(crt, 'FullName')
                            newFullName.text = self.characters[crId].fullName

                        else:
                            crt.find(
                                'FullName').text = self.characters[crId].fullName

                    majorMarker = crt.find('Major')

                    if majorMarker is not None:

                        if not self.characters[crId].isMajor:
                            crt.remove(majorMarker)

                    else:
                        if self.characters[crId].isMajor:
                            newMajor = ET.SubElement(crt, 'Major')
                            newMajor.text = '-1'

        def copyLocations():

            if novel.locations != {}:

                for lcId in novel.locations:

                    if novel.locations[lcId].title:
                        # avoids deleting the title, if it is empty by accident
                        self.locations[lcId].title = novel.locations[lcId].title

                    if novel.locations[lcId].desc is not None:
                        self.locations[lcId].desc = novel.locations[lcId].desc

                    if novel.locations[lcId].aka is not None:
                        self.locations[lcId].aka = novel.locations[lcId].aka

                    if novel.locations[lcId].tags is not None:
                        self.locations[lcId].tags = novel.locations[lcId].tags

        def writeLocations():

            for loc in root.iter('LOCATION'):
                lcId = loc.find('ID').text

                if lcId in self.locations:

                    if self.locations[lcId].title is not None:
                        loc.find('Title').text = self.locations[lcId].title

                    if self.locations[lcId].desc is not None:

                        if loc.find('Desc') is None:
                            newDesc = ET.SubElement(loc, 'Desc')
                            newDesc.text = self.locations[lcId].desc

                        else:
                            loc.find('Desc').text = self.locations[lcId].desc

                    if self.locations[lcId].aka is not None:

                        if loc.find('AKA') is None:
                            newAka = ET.SubElement(loc, 'AKA')
                            newAka.text = self.locations[lcId].aka

                        else:
                            loc.find('AKA').text = self.locations[lcId].aka

                    if self.locations[lcId].tags is not None:

                        if loc.find('Tags') is None:
                            newTags = ET.SubElement(loc, 'Tags')
                            newTags.text = ';'.join(self.locations[lcId].tags)

                        else:
                            loc.find('Tags').text = ';'.join(
                                self.locations[lcId].tags)

        def copyItems():

            if novel.items != {}:

                for itId in novel.items:

                    if novel.items[itId].title:
                        # avoids deleting the title, if it is empty by accident
                        self.items[itId].title = novel.items[itId].title

                    if novel.items[itId].desc is not None:
                        self.items[itId].desc = novel.items[itId].desc

                    if novel.items[itId].aka is not None:
                        self.items[itId].aka = novel.items[itId].aka

                    if novel.items[itId].tags is not None:
                        self.items[itId].tags = novel.items[itId].tags

        def writeItems():

            for itm in root.iter('ITEM'):
                itId = itm.find('ID').text

                if itId in self.items:

                    if self.items[itId].title is not None:
                        itm.find('Title').text = self.items[itId].title

                    if self.items[itId].desc is not None:

                        if itm.find('Desc') is None:
                            newDesc = ET.SubElement(itm, 'Desc')
                            newDesc.text = self.items[itId].desc

                        else:
                            itm.find('Desc').text = self.items[itId].desc

                    if self.items[itId].aka is not None:

                        if itm.find('AKA') is None:
                            newAka = ET.SubElement(itm, 'AKA')
                            newAka.text = self.items[itId].aka

                        else:
                            itm.find('AKA').text = self.items[itId].aka

                    if self.items[itId].tags is not None:

                        if itm.find('Tags') is None:
                            newTags = ET.SubElement(itm, 'Tags')
                            newTags.text = ';'.join(self.items[itId].tags)

                        else:
                            itm.find('Tags').text = ';'.join(
                                self.items[itId].tags)

        # Copy the novel's attributes to write.

        copyCharacters()
        copyLocations()
        copyItems()
        copyProjectLevel()
        copyChapterLevel()
        scenesTotal = copySceneLevel()

        # Overwrite the XML element tree items.

        root = self._tree.getroot()

        writeCharacters()
        writeLocations()
        writeItems()
        writeProjectLevel()
        writeChapterLevel()
        writeSceneLevel()

        indent(root)

        self._tree = ET.ElementTree(root)

        try:
            self._tree.write(
                self._filePath, xml_declaration=False, encoding=self._ENCODING)

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree.

        message = xml_postprocess(
            self._filePath, self._ENCODING, self._cdataTags)

        if message.startswith('ERROR'):
            return message

        if scenesTotal:
            info = str(scenesTotal) + ' Scenes'

        else:
            info = 'project data'

        return 'SUCCESS: ' + info + ' written to "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False
