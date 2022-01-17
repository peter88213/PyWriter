"""Provide a generic class for yWriter project import and export.

yWriter version-specific file representations inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import xml.etree.ElementTree as ET

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.character import Character
from pywriter.model.world_element import WorldElement

from pywriter.yw.yw7_tree_builder import Yw7TreeBuilder
from pywriter.yw.utf8_tree_writer import Utf8TreeWriter
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor

from pywriter.model.splitter import Splitter


class Yw7File(Novel):
    """yWriter 7 project file representation.

    Additional attributes:
        ywTreeBuilder -- strategy class to build an xml tree.
        ywTreeWriter -- strategy class to write yWriter project files.
        ywPostprocessor -- strategy class to postprocess yWriter project files.
        tree -- xml element tree of the yWriter project
    """

    DESCRIPTION = 'yWriter 7 project'
    EXTENSION = '.yw7'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables:
        Extend the superclass constructor by adding.
        """
        super().__init__(filePath)

        self.ywTreeBuilder = Yw7TreeBuilder()
        self.ywTreeWriter = Utf8TreeWriter()
        self.ywPostprocessor = Utf8Postprocessor()
        self.tree = None

    def _strip_spaces(self, lines):
        """Local helper method.

        Positional argument:
            lines -- list of strings

        Return lines with leading and trailing spaces removed.
        """
        stripped = []

        for line in lines:
            stripped.append(line.strip())

        return stripped

    def read(self):
        """Parse the yWriter xml file, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        if self.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        try:
            self.tree = ET.parse(self.filePath)

        except:
            return 'ERROR: Can not process "' + os.path.normpath(self.filePath) + '".'

        root = self.tree.getroot()

        #--- Read locations from the xml element tree.

        for loc in root.iter('LOCATION'):
            lcId = loc.find('ID').text
            self.srtLocations.append(lcId)
            self.locations[lcId] = WorldElement()

            if loc.find('Title') is not None:
                self.locations[lcId].title = loc.find('Title').text

            if loc.find('ImageFile') is not None:
                self.locations[lcId].image = loc.find('ImageFile').text

            if loc.find('Desc') is not None:
                self.locations[lcId].desc = loc.find('Desc').text

            if loc.find('AKA') is not None:
                self.locations[lcId].aka = loc.find('AKA').text

            if loc.find('Tags') is not None:

                if loc.find('Tags').text is not None:
                    tags = loc.find('Tags').text.split(';')
                    self.locations[lcId].tags = self._strip_spaces(tags)

        #--- Read items from the xml element tree.

        for itm in root.iter('ITEM'):
            itId = itm.find('ID').text
            self.srtItems.append(itId)
            self.items[itId] = WorldElement()

            if itm.find('Title') is not None:
                self.items[itId].title = itm.find('Title').text

            if itm.find('ImageFile') is not None:
                self.items[itId].image = itm.find('ImageFile').text

            if itm.find('Desc') is not None:
                self.items[itId].desc = itm.find('Desc').text

            if itm.find('AKA') is not None:
                self.items[itId].aka = itm.find('AKA').text

            if itm.find('Tags') is not None:

                if itm.find('Tags').text is not None:
                    tags = itm.find('Tags').text.split(';')
                    self.items[itId].tags = self._strip_spaces(tags)

        #--- Read characters from the xml element tree.

        for crt in root.iter('CHARACTER'):
            crId = crt.find('ID').text
            self.srtCharacters.append(crId)
            self.characters[crId] = Character()

            if crt.find('Title') is not None:
                self.characters[crId].title = crt.find('Title').text

            if crt.find('ImageFile') is not None:
                self.characters[crId].image = crt.find('ImageFile').text

            if crt.find('Desc') is not None:
                self.characters[crId].desc = crt.find('Desc').text

            if crt.find('AKA') is not None:
                self.characters[crId].aka = crt.find('AKA').text

            if crt.find('Tags') is not None:

                if crt.find('Tags').text is not None:
                    tags = crt.find('Tags').text.split(';')
                    self.characters[crId].tags = self._strip_spaces(tags)

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

        #--- Read attributes at novel level from the xml element tree.

        prj = root.find('PROJECT')

        if prj.find('Title') is not None:
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

        #--- Read attributes at chapter level from the xml element tree.

        self.srtChapters = []
        # This is necessary for re-reading.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.srtChapters.append(chId)

            if chp.find('Title') is not None:
                self.chapters[chId].title = chp.find('Title').text

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

            self.chapters[chId].suppressChapterTitle = False

            if self.chapters[chId].title is not None:

                if self.chapters[chId].title.startswith('@'):
                    self.chapters[chId].suppressChapterTitle = True

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

        #--- Read attributes at scene level from the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text
            self.scenes[scId] = Scene()

            if scn.find('Title') is not None:
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

            self.scenes[scId].isNotesScene = False
            self.scenes[scId].isTodoScene = False

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
                    tags = scn.find('Tags').text.split(';')
                    self.scenes[scId].tags = self._strip_spaces(tags)

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

            if scn.find('ImageFile') is not None:
                self.scenes[scId].image = scn.find('ImageFile').text

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

        # Make sure that ToDo, Notes, and Unused type is inherited from the
        # chapter.

        for chId in self.chapters:

            if self.chapters[chId].chType == 2:
                # Chapter is "ToDo" type.

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isTodoScene = True
                    self.scenes[scId].isUnused = True

            elif self.chapters[chId].chType == 1:
                # Chapter is "Notes" type.

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isNotesScene = True
                    self.scenes[scId].isUnused = True

            elif self.chapters[chId].isUnused:

                for scId in self.chapters[chId].srtScenes:
                    self.scenes[scId].isUnused = True

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + os.path.normpath(self.filePath) + '".'

    def merge(self, source):
        """Copy required attributes of the source object.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        def merge_lists(srcLst, tgtLst):
            """Insert srcLst items to tgtLst, if missing.
            """
            j = 0

            for i in range(len(srcLst)):

                if not srcLst[i] in tgtLst:
                    tgtLst.insert(j, srcLst[i])
                    j += 1

                else:
                    j = tgtLst.index(srcLst[i]) + 1

        if os.path.isfile(self.filePath):
            message = self.read()
            # initialize data

            if message.startswith('ERROR'):
                return message

        #--- Merge and re-order locations.

        if source.srtLocations != []:
            self.srtLocations = source.srtLocations
            temploc = self.locations
            self.locations = {}

            for lcId in source.srtLocations:

                # Build a new self.locations dictionary sorted like the
                # source

                self.locations[lcId] = WorldElement()

                if not lcId in temploc:
                    # A new location has been added
                    temploc[lcId] = WorldElement()

                if source.locations[lcId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.locations[lcId].title = source.locations[lcId].title

                else:
                    self.locations[lcId].title = temploc[lcId].title

                if source.locations[lcId].image is not None:
                    self.locations[lcId].image = source.locations[lcId].image

                else:
                    self.locations[lcId].desc = temploc[lcId].desc

                if source.locations[lcId].desc is not None:
                    self.locations[lcId].desc = source.locations[lcId].desc

                else:
                    self.locations[lcId].desc = temploc[lcId].desc

                if source.locations[lcId].aka is not None:
                    self.locations[lcId].aka = source.locations[lcId].aka

                else:
                    self.locations[lcId].aka = temploc[lcId].aka

                if source.locations[lcId].tags is not None:
                    self.locations[lcId].tags = source.locations[lcId].tags

                else:
                    self.locations[lcId].tags = temploc[lcId].tags

        #--- Merge and re-order items.

        if source.srtItems != []:
            self.srtItems = source.srtItems
            tempitm = self.items
            self.items = {}

            for itId in source.srtItems:

                # Build a new self.items dictionary sorted like the
                # source

                self.items[itId] = WorldElement()

                if not itId in tempitm:
                    # A new item has been added
                    tempitm[itId] = WorldElement()

                if source.items[itId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.items[itId].title = source.items[itId].title

                else:
                    self.items[itId].title = tempitm[itId].title

                if source.items[itId].image is not None:
                    self.items[itId].image = source.items[itId].image

                else:
                    self.items[itId].image = tempitm[itId].image

                if source.items[itId].desc is not None:
                    self.items[itId].desc = source.items[itId].desc

                else:
                    self.items[itId].desc = tempitm[itId].desc

                if source.items[itId].aka is not None:
                    self.items[itId].aka = source.items[itId].aka

                else:
                    self.items[itId].aka = tempitm[itId].aka

                if source.items[itId].tags is not None:
                    self.items[itId].tags = source.items[itId].tags

                else:
                    self.items[itId].tags = tempitm[itId].tags

        #--- Merge and re-order characters.

        if source.srtCharacters != []:
            self.srtCharacters = source.srtCharacters
            tempchr = self.characters
            self.characters = {}

            for crId in source.srtCharacters:

                # Build a new self.characters dictionary sorted like the
                # source

                self.characters[crId] = Character()

                if not crId in tempchr:
                    # A new character has been added
                    tempchr[crId] = Character()

                if source.characters[crId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.characters[crId].title = source.characters[crId].title

                else:
                    self.characters[crId].title = tempchr[crId].title

                if source.characters[crId].image is not None:
                    self.characters[crId].image = source.characters[crId].image

                else:
                    self.characters[crId].image = tempchr[crId].image

                if source.characters[crId].desc is not None:
                    self.characters[crId].desc = source.characters[crId].desc

                else:
                    self.characters[crId].desc = tempchr[crId].desc

                if source.characters[crId].aka is not None:
                    self.characters[crId].aka = source.characters[crId].aka

                else:
                    self.characters[crId].aka = tempchr[crId].aka

                if source.characters[crId].tags is not None:
                    self.characters[crId].tags = source.characters[crId].tags

                else:
                    self.characters[crId].tags = tempchr[crId].tags

                if source.characters[crId].notes is not None:
                    self.characters[crId].notes = source.characters[crId].notes

                else:
                    self.characters[crId].notes = tempchr[crId].notes

                if source.characters[crId].bio is not None:
                    self.characters[crId].bio = source.characters[crId].bio

                else:
                    self.characters[crId].bio = tempchr[crId].bio

                if source.characters[crId].goals is not None:
                    self.characters[crId].goals = source.characters[crId].goals

                else:
                    self.characters[crId].goals = tempchr[crId].goals

                if source.characters[crId].fullName is not None:
                    self.characters[crId].fullName = source.characters[crId].fullName

                else:
                    self.characters[crId].fullName = tempchr[crId].fullName

                if source.characters[crId].isMajor is not None:
                    self.characters[crId].isMajor = source.characters[crId].isMajor

                else:
                    self.characters[crId].isMajor = tempchr[crId].isMajor

        #--- Merge scenes.

        sourceHasSceneContent = False

        for scId in source.scenes:

            if not scId in self.scenes:
                self.scenes[scId] = Scene()

            if source.scenes[scId].title:
                # avoids deleting the title, if it is empty by accident
                self.scenes[scId].title = source.scenes[scId].title

            if source.scenes[scId].desc is not None:
                self.scenes[scId].desc = source.scenes[scId].desc

            if source.scenes[scId].sceneContent is not None:
                self.scenes[scId].sceneContent = source.scenes[scId].sceneContent
                sourceHasSceneContent = True

            if source.scenes[scId].isUnused is not None:
                self.scenes[scId].isUnused = source.scenes[scId].isUnused

            if source.scenes[scId].isNotesScene is not None:
                self.scenes[scId].isNotesScene = source.scenes[scId].isNotesScene

            if source.scenes[scId].isTodoScene is not None:
                self.scenes[scId].isTodoScene = source.scenes[scId].isTodoScene

            if source.scenes[scId].status is not None:
                self.scenes[scId].status = source.scenes[scId].status

            if source.scenes[scId].sceneNotes is not None:
                self.scenes[scId].sceneNotes = source.scenes[scId].sceneNotes

            if source.scenes[scId].tags is not None:
                self.scenes[scId].tags = source.scenes[scId].tags

            if source.scenes[scId].field1 is not None:
                self.scenes[scId].field1 = source.scenes[scId].field1

            if source.scenes[scId].field2 is not None:
                self.scenes[scId].field2 = source.scenes[scId].field2

            if source.scenes[scId].field3 is not None:
                self.scenes[scId].field3 = source.scenes[scId].field3

            if source.scenes[scId].field4 is not None:
                self.scenes[scId].field4 = source.scenes[scId].field4

            if source.scenes[scId].appendToPrev is not None:
                self.scenes[scId].appendToPrev = source.scenes[scId].appendToPrev

            if source.scenes[scId].date or source.scenes[scId].time:

                if source.scenes[scId].date is not None:
                    self.scenes[scId].date = source.scenes[scId].date

                if source.scenes[scId].time is not None:
                    self.scenes[scId].time = source.scenes[scId].time

            elif source.scenes[scId].minute or source.scenes[scId].hour or source.scenes[scId].day:
                self.scenes[scId].date = None
                self.scenes[scId].time = None

            if source.scenes[scId].minute is not None:
                self.scenes[scId].minute = source.scenes[scId].minute

            if source.scenes[scId].hour is not None:
                self.scenes[scId].hour = source.scenes[scId].hour

            if source.scenes[scId].day is not None:
                self.scenes[scId].day = source.scenes[scId].day

            if source.scenes[scId].lastsMinutes is not None:
                self.scenes[scId].lastsMinutes = source.scenes[scId].lastsMinutes

            if source.scenes[scId].lastsHours is not None:
                self.scenes[scId].lastsHours = source.scenes[scId].lastsHours

            if source.scenes[scId].lastsDays is not None:
                self.scenes[scId].lastsDays = source.scenes[scId].lastsDays

            if source.scenes[scId].isReactionScene is not None:
                self.scenes[scId].isReactionScene = source.scenes[scId].isReactionScene

            if source.scenes[scId].isSubPlot is not None:
                self.scenes[scId].isSubPlot = source.scenes[scId].isSubPlot

            if source.scenes[scId].goal is not None:
                self.scenes[scId].goal = source.scenes[scId].goal

            if source.scenes[scId].conflict is not None:
                self.scenes[scId].conflict = source.scenes[scId].conflict

            if source.scenes[scId].outcome is not None:
                self.scenes[scId].outcome = source.scenes[scId].outcome

            if source.scenes[scId].characters is not None:
                self.scenes[scId].characters = []

                for crId in source.scenes[scId].characters:

                    if crId in self.characters:
                        self.scenes[scId].characters.append(crId)

            if source.scenes[scId].locations is not None:
                self.scenes[scId].locations = []

                for lcId in source.scenes[scId].locations:

                    if lcId in self.locations:
                        self.scenes[scId].locations.append(lcId)

            if source.scenes[scId].items is not None:
                self.scenes[scId].items = []

                for itId in source.scenes[scId].items:

                    if itId in self.items:
                        self.scenes[scId].items.append(itId)

        #--- Merge chapters.

        for chId in source.chapters:

            if not chId in self.chapters:
                self.chapters[chId] = Chapter()

            if source.chapters[chId].title:
                # avoids deleting the title, if it is empty by accident
                self.chapters[chId].title = source.chapters[chId].title

            if source.chapters[chId].desc is not None:
                self.chapters[chId].desc = source.chapters[chId].desc

            if source.chapters[chId].chLevel is not None:
                self.chapters[chId].chLevel = source.chapters[chId].chLevel

            if source.chapters[chId].oldType is not None:
                self.chapters[chId].oldType = source.chapters[chId].oldType

            if source.chapters[chId].chType is not None:
                self.chapters[chId].chType = source.chapters[chId].chType

            if source.chapters[chId].isUnused is not None:
                self.chapters[chId].isUnused = source.chapters[chId].isUnused

            if source.chapters[chId].suppressChapterTitle is not None:
                self.chapters[chId].suppressChapterTitle = source.chapters[chId].suppressChapterTitle

            if source.chapters[chId].suppressChapterBreak is not None:
                self.chapters[chId].suppressChapterBreak = source.chapters[chId].suppressChapterBreak

            if source.chapters[chId].isTrash is not None:
                self.chapters[chId].isTrash = source.chapters[chId].isTrash

            #--- Merge the chapter's scene list.
            # New scenes may be added.
            # Existing scenes may be moved to another chapter.
            # Deletion of scenes is not considered.
            # The scene's sort order may not change.

            if source.chapters[chId].srtScenes is not None:

                # Remove scenes that have been moved to another chapter from the scene list.

                srtScenes = []

                for scId in self.chapters[chId].srtScenes:

                    if scId in source.chapters[chId].srtScenes or not scId in source.scenes:
                        srtScenes.append(scId)
                        # The scene has not moved to another chapter or isn't imported

                    self.chapters[chId].srtScenes = srtScenes

                # Add new or moved scenes to the scene list.

                merge_lists(source.chapters[chId].srtScenes, self.chapters[chId].srtScenes)

        #--- Merge project attributes.

        if source.title:
            # avoids deleting the title, if it is empty by accident
            self.title = source.title

        if source.desc is not None:
            self.desc = source.desc

        if source.author is not None:
            self.author = source.author

        if source.fieldTitle1 is not None:
            self.fieldTitle1 = source.fieldTitle1

        if source.fieldTitle2 is not None:
            self.fieldTitle2 = source.fieldTitle2

        if source.fieldTitle3 is not None:
            self.fieldTitle3 = source.fieldTitle3

        if source.fieldTitle4 is not None:
            self.fieldTitle4 = source.fieldTitle4

        # Add new chapters to the chapter list.
        # Deletion of chapters is not considered.
        # The sort order of chapters may not change.

        merge_lists(source.srtChapters, self.srtChapters)

        # Split scenes by inserted part/chapter/scene dividers.
        # This must be done after regular merging
        # in order to avoid creating duplicate IDs.

        if sourceHasSceneContent:
            sceneSplitter = Splitter()
            sceneSplitter.split_scenes(self)

        return 'SUCCESS'

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        if self.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        message = self.ywTreeBuilder.build_element_tree(self)

        if message.startswith('ERROR'):
            return message

        message = self.ywTreeWriter.write_element_tree(self)

        if message.startswith('ERROR'):
            return message

        return self.ywPostprocessor.postprocess_xml_file(self.filePath)

    def is_locked(self):
        """Return True if a .lock file placed by yWriter exists.
        Otherwise, return False. 
        """
        return os.path.isfile(self.filePath + '.lock')
