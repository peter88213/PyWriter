"""yWFile - Class for yWriter 7 xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.object import Object


class YwFile(Novel):
    """yWriter xml project file representation."""

    def read(self):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        if self.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        message = self.ywTreeReader.read_element_tree(self)

        if message.startswith('ERROR'):
            return message

        root = self._tree.getroot()

        # Read locations from the xml element tree.

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

        # Read items from the xml element tree.

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

        # Read characters from the xml element tree.

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

        # Read attributes at novel level from the xml element tree.

        prj = root.find('PROJECT')
        self.title = prj.find('Title').text

        if prj.find('AuthorName') is not None:
            self.author = prj.find('AuthorName').text

        if prj.find('Desc') is not None:
            self.desc = prj.find('Desc').text

        if prj.find('FieldTitle1') is not None:
            self.fieldTitle1 = prj.find('FieldTitle1').text

        if prj.find('FieldTitle2') is not None:
            self.fieldTitle2 = prj.find('FieldTitle2').text

        if prj.find('FieldTitle3') is not None:
            self.fieldTitle3 = prj.find('FieldTitle3').text

        if prj.find('FieldTitle4') is not None:
            self.fieldTitle4 = prj.find('FieldTitle4').text

        # Read attributes at chapter level from the xml element tree.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.srtChapters.append(chId)

            self.chapters[chId].title = chp.find('Title').text

            if self.chapters[chId].title.startswith('@'):
                self.chapters[chId].suppressChapterTitle = True

            else:
                self.chapters[chId].suppressChapterTitle = False

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            if chp.find('Type') is not None:
                self.chapters[chId].oldType = int(chp.find('Type').text)

            if chp.find('ChapterType') is not None:
                self.chapters[chId].chType = int(chp.find('ChapterType').text)

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

            for chFields in chp.findall('Fields'):

                if chFields.find('Field_SuppressChapterTitle') is not None:

                    if chFields.find('Field_SuppressChapterTitle').text == '1':
                        self.chapters[chId].suppressChapterTitle = True

                if chFields.find('Field_IsTrash') is not None:

                    if chFields.find('Field_IsTrash').text == '1':
                        self.chapters[chId].isTrash = True

                    else:
                        self.chapters[chId].isTrash = False

                if chFields.find('Field_SuppressChapterBreak') is not None:

                    if chFields.find('Field_SuppressChapterBreak').text == '1':
                        self.chapters[chId].suppressChapterBreak = True

                    else:
                        self.chapters[chId].suppressChapterBreak = False

                else:
                    self.chapters[chId].suppressChapterBreak = False

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                if not self.chapters[chId].isTrash:

                    for scn in chp.find('Scenes').findall('ScID'):
                        scId = scn.text
                        self.chapters[chId].srtScenes.append(scId)

        # Read attributes at scene level from the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text
            self.scenes[scId] = Scene()

            self.scenes[scId].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scId].desc = scn.find('Desc').text

            if scn.find('RTFFile') is not None:
                self.scenes[scId].rtfFile = scn.find('RTFFile').text

            # This is relevant for yW5 files with no SceneContent:

            if scn.find('WordCount') is not None:
                self.scenes[scId].wordCount = int(
                    scn.find('WordCount').text)

            if scn.find('LetterCount') is not None:
                self.scenes[scId].letterCount = int(
                    scn.find('LetterCount').text)

            if scn.find('SceneContent') is not None:
                sceneContent = scn.find('SceneContent').text

                if sceneContent is not None:
                    self.scenes[scId].sceneContent = sceneContent

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            else:
                self.scenes[scId].isUnused = False

            for scFields in scn.findall('Fields'):

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '1':
                        self.scenes[scId].isNotesScene = True

                    if scFields.find('Field_SceneType').text == '2':
                        self.scenes[scId].isTodoScene = True

            if scn.find('ExportCondSpecific') is None:
                self.scenes[scId].doNotExport = False

            elif scn.find('ExportWhenRTF') is not None:
                self.scenes[scId].doNotExport = False

            else:
                self.scenes[scId].doNotExport = True

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

            if scn.find('SpecificDateTime') is not None:
                dateTime = scn.find('SpecificDateTime').text.split(' ')

                for dt in dateTime:

                    if '-' in dt:
                        self.scenes[scId].date = dt

                    elif ':' in dt:
                        self.scenes[scId].time = dt

            else:
                if scn.find('Day') is not None:
                    self.scenes[scId].day = scn.find('Day').text

                if scn.find('Hour') is not None:
                    self.scenes[scId].hour = scn.find('Hour').text

                if scn.find('Minute') is not None:
                    self.scenes[scId].minute = scn.find('Minute').text

            if scn.find('LastsDays') is not None:
                self.scenes[scId].lastsDays = scn.find('LastsDays').text

            if scn.find('LastsHours') is not None:
                self.scenes[scId].lastsHours = scn.find('LastsHours').text

            if scn.find('LastsMinutes') is not None:
                self.scenes[scId].lastsMinutes = scn.find('LastsMinutes').text

            if scn.find('ReactionScene') is not None:
                self.scenes[scId].isReactionScene = True

            else:
                self.scenes[scId].isReactionScene = False

            if scn.find('SubPlot') is not None:
                self.scenes[scId].isSubPlot = True

            else:
                self.scenes[scId].isSubPlot = False

            if scn.find('Goal') is not None:
                self.scenes[scId].goal = scn.find('Goal').text

            if scn.find('Conflict') is not None:
                self.scenes[scId].conflict = scn.find('Conflict').text

            if scn.find('Outcome') is not None:
                self.scenes[scId].outcome = scn.find('Outcome').text

            if scn.find('Characters') is not None:
                for crId in scn.find('Characters').iter('CharID'):

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    self.scenes[scId].characters.append(crId.text)

            if scn.find('Locations') is not None:
                for lcId in scn.find('Locations').iter('LocID'):

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    self.scenes[scId].locations.append(lcId.text)

            if scn.find('Items') is not None:
                for itId in scn.find('Items').iter('ItemID'):

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    self.scenes[scId].items.append(itId.text)

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def merge(self, novel):
        """Merge attributes.
        """

        if self.file_exists():
            message = self.read()
            # initialize data

            if message.startswith('ERROR'):
                return message

        if novel.get_structure() == '':
            return 'ERROR: Source file contains nothing to write to a yWriter project.'

        # Merge locations.

        for lcId in novel.locations:

            if not lcId in self.locations:
                self.locations[lcId] = Object()

            if novel.locations[lcId].title:
                # avoids deleting the title, if it is empty by accident
                self.locations[lcId].title = novel.locations[lcId].title

            if novel.locations[lcId].desc is not None:
                self.locations[lcId].desc = novel.locations[lcId].desc

            if novel.locations[lcId].aka is not None:
                self.locations[lcId].aka = novel.locations[lcId].aka

            if novel.locations[lcId].tags is not None:
                self.locations[lcId].tags = novel.locations[lcId].tags

        # Merge items.

        for itId in novel.items:

            if not itId in self.items:
                self.items[itId] = Object()

            if novel.items[itId].title:
                # avoids deleting the title, if it is empty by accident
                self.items[itId].title = novel.items[itId].title

            if novel.items[itId].desc is not None:
                self.items[itId].desc = novel.items[itId].desc

            if novel.items[itId].aka is not None:
                self.items[itId].aka = novel.items[itId].aka

            if novel.items[itId].tags is not None:
                self.items[itId].tags = novel.items[itId].tags

        # Merge characters.

        for crId in novel.characters:

            if not crId in self.characters:
                self.characters[crId] = Character()

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

        # Merge scenes.

        for scId in novel.scenes:

            if not scId in self.scenes:
                self.scenes[scId] = Scene()

            if novel.scenes[scId].title:
                # avoids deleting the title, if it is empty by accident
                self.scenes[scId].title = novel.scenes[scId].title

            if novel.scenes[scId].desc is not None:
                self.scenes[scId].desc = novel.scenes[scId].desc

            if novel.scenes[scId].sceneContent is not None:
                self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

            if novel.scenes[scId].rtfFile is not None:
                self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

            if novel.scenes[scId].isUnused is not None:
                self.scenes[scId].isUnused = novel.scenes[scId].isUnused

            if novel.scenes[scId].isNotesScene is not None:
                self.scenes[scId].isNotesScene = novel.scenes[scId].isNotesScene

            if novel.scenes[scId].isTodoScene is not None:
                self.scenes[scId].isTodoScene = novel.scenes[scId].isTodoScene

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

            if novel.scenes[scId].date is not None:
                self.scenes[scId].date = novel.scenes[scId].date

            if novel.scenes[scId].time is not None:
                self.scenes[scId].time = novel.scenes[scId].time

            if novel.scenes[scId].minute is not None:
                self.scenes[scId].minute = novel.scenes[scId].minute

            if novel.scenes[scId].hour is not None:
                self.scenes[scId].hour = novel.scenes[scId].hour

            if novel.scenes[scId].day is not None:
                self.scenes[scId].day = novel.scenes[scId].day

            if novel.scenes[scId].lastsMinutes is not None:
                self.scenes[scId].lastsMinutes = novel.scenes[scId].lastsMinutes

            if novel.scenes[scId].lastsHours is not None:
                self.scenes[scId].lastsHours = novel.scenes[scId].lastsHours

            if novel.scenes[scId].lastsDays is not None:
                self.scenes[scId].lastsDays = novel.scenes[scId].lastsDays

            if novel.scenes[scId].isReactionScene is not None:
                self.scenes[scId].isReactionScene = novel.scenes[scId].isReactionScene

            if novel.scenes[scId].isSubPlot is not None:
                self.scenes[scId].isSubPlot = novel.scenes[scId].isSubPlot

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
                        self.scenes[scId].append(itId)

        # Merge chapters.

        scenesAssigned = []

        for chId in novel.chapters:

            if not chId in self.chapters:
                self.chapters[chId] = Chapter()

            if novel.chapters[chId].title:
                # avoids deleting the title, if it is empty by accident
                self.chapters[chId].title = novel.chapters[chId].title

            if novel.chapters[chId].desc is not None:
                self.chapters[chId].desc = novel.chapters[chId].desc

            if novel.chapters[chId].chLevel is not None:
                self.chapters[chId].chLevel = novel.chapters[chId].chLevel

            if novel.chapters[chId].oldType is not None:
                self.chapters[chId].oldType = novel.chapters[chId].oldType

            if novel.chapters[chId].chType is not None:
                self.chapters[chId].chType = novel.chapters[chId].chType

            if novel.chapters[chId].isUnused is not None:
                self.chapters[chId].isUnused = novel.chapters[chId].isUnused

            if novel.chapters[chId].suppressChapterTitle is not None:
                self.chapters[chId].suppressChapterTitle = novel.chapters[chId].suppressChapterTitle

            if novel.chapters[chId].suppressChapterBreak is not None:
                self.chapters[chId].suppressChapterBreak = novel.chapters[chId].suppressChapterBreak

            if novel.chapters[chId].isTrash is not None:
                self.chapters[chId].isTrash = novel.chapters[chId].isTrash

            if novel.chapters[chId].srtScenes is not None:
                self.chapters[chId].srtScenes = []

                for scId in novel.chapters[chId].srtScenes:

                    if (scId in self.scenes) and not (scId in scenesAssigned):
                        self.chapters[chId].srtScenes.append(scId)
                        scenesAssigned.append(scId)

        # Merge attributes at novel level.

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

        if novel.srtChapters != []:
            self.srtChapters = []

            for chId in novel.srtChapters:

                if chId in self.chapters:
                    self.srtChapters.append(chId)

        return 'SUCCESS'

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        if self.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        message = self.ywTreeBuilder.build_element_tree(self)

        if message.startswith('ERROR'):
            return message

        message = self.ywTreeWriter.write_element_tree(self)

        if message.startswith('ERROR'):
            return message

        message = self.ywPostprocessor.postprocess_xml_file(self.filePath)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: "' + os.path.normpath(self.filePath) + '" written.'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self.filePath + '.lock'):
            return True

        else:
            return False
