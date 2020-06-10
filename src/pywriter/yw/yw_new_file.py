"""yWNewFile - Class for yWriter xml file creation.

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
from pywriter.yw.yw_form import *


class YwNewFile(Novel):
    """yWriter xml project file representation."""

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc',
                           'FieldTitle1', 'FieldTitle2', 'FieldTitle3',
                           'FieldTitle4', 'LaTeXHeaderFile', 'Tags',
                           'AKA', 'ImageFile', 'FullName', 'Goals',
                           'Notes', 'RTFFile', 'SceneContent',
                           'Outcome', 'Goal', 'Conflict']
        # Names of yWriter xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the correct extension. """

        if filePath.lower().endswith('.yw7'):
            self._FILE_EXTENSION = '.yw7'
            self._ENCODING = 'utf-8'
            self._filePath = filePath

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        # Merge locations.

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

        # Merge items.

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

        # Merge characters.

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

        self.srtChapters = novel.srtChapters

        # Merge attributes at chapter level.

        if novel.chapters != {}:

            for chId in novel.chapters:
                self.chapters[chId] = Chapter()

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

                if novel.chapters[chId].isTrash is not None:
                    self.chapters[chId].isTrash = novel.chapters[chId].isTrash

                if novel.chapters[chId].srtScenes != []:
                    self.chapters[chId].srtScenes = novel.chapters[chId].srtScenes

        # Merge attributes at scene level.

        if novel.scenes != {}:

            for scId in novel.scenes:
                self.scenes[scId] = Scene()

                if novel.scenes[scId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].desc is not None:
                    self.scenes[scId].desc = novel.scenes[scId].desc

                if novel.scenes[scId].sceneContent is not None:
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

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
                            self.scenes[scId].append(crId)

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        root = ET.Element('YWRITER7')

        # Write attributes at novel level to the xml element tree.

        prj = ET.SubElement(root, 'PROJECT')
        ET.SubElement(prj, 'Ver').text = '7'

        if self.title is not None:
            ET.SubElement(prj, 'Title').text = self.title

        if self.desc is not None:
            ET.SubElement(prj, 'Desc').text = self.desc

        if self.author is not None:
            ET.SubElement(prj, 'AuthorName').text = self.author

        if self.fieldTitle1 is not None:
            ET.SubElement(prj, 'FieldTitle1').text = self.fieldTitle1

        if self.fieldTitle2 is not None:
            ET.SubElement(prj, 'FieldTitle2').text = self.fieldTitle2

        if self.fieldTitle3 is not None:
            ET.SubElement(prj, 'FieldTitle3').text = self.fieldTitle3

        if self.fieldTitle4 is not None:
            ET.SubElement(prj, 'FieldTitle4').text = self.fieldTitle4

        # Write locations to the xml element tree.

        locations = ET.SubElement(root, 'LOCATIONS')

        for lcId in self.locations:
            loc = ET.SubElement(locations, 'LOCATION')
            ET.SubElement(loc, 'ID').text = lcId

            if self.locations[lcId].title is not None:
                ET.SubElement(loc, 'Title').text = self.locations[lcId].title

            if self.locations[lcId].desc is not None:
                ET.SubElement(loc, 'Desc').text = self.locations[lcId].desc

            if self.locations[lcId].aka is not None:
                ET.SubElement(loc, 'AKA').text = self.locations[lcId].aka

            if self.locations[lcId].tags is not None:
                ET.SubElement(loc, 'Tags').text = ';'.join(
                    self.locations[lcId].tags)

        # Write items to the xml element tree.

        items = ET.SubElement(root, 'ITEMS')

        for itId in self.items:
            itm = ET.SubElement(items, 'ITEM')
            ET.SubElement(itm, 'ID').text = itId

            if self.items[itId].title is not None:
                ET.SubElement(itm, 'Title').text = self.items[itId].title

            if self.items[itId].desc is not None:
                ET.SubElement(itm, 'Desc').text = self.items[itId].desc

            if self.items[itId].aka is not None:
                ET.SubElement(itm, 'AKA').text = self.items[itId].aka

            if self.items[itId].tags is not None:
                ET.SubElement(itm, 'Tags').text = ';'.join(
                    self.items[itId].tags)

        # Write characters to the xml element tree.

        characters = ET.SubElement(root, 'CHARACTERS')

        for crId in self.characters:
            crt = ET.SubElement(characters, 'CHARACTER')
            ET.SubElement(crt, 'ID').text = crId

            if self.characters[crId].title is not None:
                ET.SubElement(
                    crt, 'Title').text = self.characters[crId].title

            if self.characters[crId].desc is not None:
                ET.SubElement(
                    crt, 'Desc').text = self.characters[crId].desc

            if self.characters[crId].aka is not None:
                ET.SubElement(crt, 'AKA').text = self.characters[crId].aka

            if self.characters[crId].tags is not None:
                ET.SubElement(crt, 'Tags').text = ';'.join(
                    self.characters[crId].tags)

            if self.characters[crId].notes is not None:
                ET.SubElement(
                    crt, 'Notes').text = self.characters[crId].notes

            if self.characters[crId].bio is not None:
                ET.SubElement(crt, 'Bio').text = self.characters[crId].bio

            if self.characters[crId].goals is not None:
                ET.SubElement(
                    crt, 'Goals').text = self.characters[crId].goals

            if self.characters[crId].fullName is not None:
                ET.SubElement(
                    crt, 'FullName').text = self.characters[crId].fullName

            if self.characters[crId].isMajor:
                ET.SubElement(crt, 'Major').text = '-1'

        # Write attributes at scene level to the xml element tree.

        scenes = ET.SubElement(root, 'SCENES')

        for scId in self.scenes:
            scn = ET.SubElement(scenes, 'SCENE')
            ET.SubElement(scn, 'ID').text = scId

            if self.scenes[scId].title is not None:
                ET.SubElement(scn, 'Title').text = self.scenes[scId].title

            if self.scenes[scId].desc is not None:
                ET.SubElement(scn, 'Desc').text = self.scenes[scId].desc

            if self.scenes[scId]._sceneContent is not None:
                ET.SubElement(scn,
                              'SceneContent').text = replace_unsafe_glyphs(self.scenes[scId]._sceneContent)
                ET.SubElement(scn, 'WordCount').text = str(
                    self.scenes[scId].wordCount)
                ET.SubElement(scn, 'LetterCount').text = str(
                    self.scenes[scId].letterCount)

            if self.scenes[scId].isUnused:
                ET.SubElement(scn, 'Unused').text = '-1'

            if self.scenes[scId].status is not None:
                ET.SubElement(scn, 'Status').text = str(
                    self.scenes[scId].status)

            if self.scenes[scId].sceneNotes is not None:
                ET.SubElement(scn, 'Notes').text = self.scenes[scId].sceneNotes

            if self.scenes[scId].tags is not None:
                ET.SubElement(scn, 'Tags').text = ';'.join(
                    self.scenes[scId].tags)

            if self.scenes[scId].field1 is not None:
                ET.SubElement(scn, 'Field1').text = self.scenes[scId].field1

            if self.scenes[scId].field2 is not None:
                ET.SubElement(scn, 'Field2').text = self.scenes[scId].field2

            if self.scenes[scId].field3 is not None:
                ET.SubElement(scn, 'Field3').text = self.scenes[scId].field3

            if self.scenes[scId].field4 is not None:
                ET.SubElement(scn, 'Field4').text = self.scenes[scId].field4

            if self.scenes[scId].appendToPrev:
                ET.SubElement(scn, 'AppendToPrev').text = '-1'

            if self.scenes[scId].isReactionScene:
                ET.SubElement(scn, 'ReactionScene').text = '-1'

            if self.scenes[scId].isSubPlot:
                ET.SubElement(scn, 'SubPlot').text = '-1'

            if self.scenes[scId].goal is not None:
                ET.SubElement(scn, 'Goal').text = self.scenes[scId].goal

            if self.scenes[scId].conflict is not None:
                ET.SubElement(
                    scn, 'Conflict').text = self.scenes[scId].conflict

            if self.scenes[scId].outcome is not None:
                ET.SubElement(scn, 'Outcome').text = self.scenes[scId].outcome

            if self.scenes[scId].characters is not None:
                scCharacters = ET.SubElement(scn, 'Characters')

                for crId in self.scenes[scId].characters:
                    ET.SubElement(scCharacters, 'CharID').text = crId

            if self.scenes[scId].locations is not None:
                scLocations = ET.SubElement(scn, 'Locations')

                for lcId in self.scenes[scId].locations:
                    ET.SubElement(scLocations, 'LocID').text = lcId

            if self.scenes[scId].items is not None:
                scItems = ET.SubElement(scn, 'Items')

                for itId in self.scenes[scId].items:
                    ET.SubElement(scItems, 'ItemID').text = itId

        # Write attributes at chapter level to the xml element tree.

        chapters = ET.SubElement(root, 'CHAPTERS')

        for chId in self.srtChapters:
            chp = ET.SubElement(chapters, 'CHAPTER')
            ET.SubElement(chp, 'ID').text = chId

            if self.chapters[chId].title is not None:
                ET.SubElement(chp, 'Title').text = self.chapters[chId].title

            if self.chapters[chId].desc is not None:
                ET.SubElement(chp, 'Desc').text = self.chapters[chId].desc

            if self.chapters[chId].chLevel == 1:
                ET.SubElement(chp, 'SectionStart').text = '-1'

            if self.chapters[chId].chType is not None:
                ET.SubElement(chp, 'Type').text = str(
                    self.chapters[chId].chType)

            if self.chapters[chId].isUnused:
                ET.SubElement(chp, 'Unused').text = '-1'

            sortSc = ET.SubElement(chp, 'Scenes')

            for scId in self.chapters[chId].srtScenes:
                ET.SubElement(sortSc, 'ScID').text = scId

            chFields = ET.SubElement(chp, 'Fields')

            if self.chapters[chId].suppressChapterTitle:
                ET.SubElement(
                    chFields, 'Field_SuppressChapterTitle').text = '1'

        # Pretty print the xml tree.

        indent(root)

        # Save the xml tree in a file.

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

        return 'SUCCESS: project data written to "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False
