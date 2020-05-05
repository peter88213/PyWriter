"""yW5File - Class for yWriter 5 xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET

from pywriter.model.novel import Novel
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.yw5.yw5_form import *


class Yw5File(Novel):
    """yWriter 5 xml project file representation."""

    _FILE_EXTENSION = '.yw5'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']
        # Names of yw7 xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    def read(self):
        """Parse the yw7 xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Complete list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r') as f:
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

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            for fields in chp.iter('Fields'):

                if fields.find('Field_SuppressChapterTitle') is not None:

                    if fields.find('Field_SuppressChapterTitle').text == '1':
                        self.chapters[chId].suppressChapterTitle = True

                    else:
                        self.chapters[chId].suppressChapterTitle = False

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

            self.chapters[chId].chType = int(chp.find('Type').text)

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                for scn in chp.find('Scenes').findall('ScID'):
                    scId = scn.text
                    self.chapters[chId].srtScenes.append(scId)

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            self.scenes[scId] = Scene()
            self.scenes[scId].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scId].desc = scn.find('Desc').text

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

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

            if scn.find('Tags') is not None:

                if scn.find('Tags').text is not None:
                    self.scenes[scId].tags = scn.find('Tags').text.split(';')

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True
            '''
            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent
            '''
        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel):
        """Open the yw7 xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the novel's attributes to write.

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

        sceneCount = 0

        if novel.scenes != {}:

            for scId in novel.scenes:

                if novel.scenes[scId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].desc is not None:
                    self.scenes[scId].desc = novel.scenes[scId].desc
                '''
                if novel.scenes[scId].sceneContent is not None:
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent
                    sceneCount += 1
                '''
                if novel.scenes[scId].sceneNotes is not None:
                    self.scenes[scId].sceneNotes = novel.scenes[scId].sceneNotes

                if novel.scenes[scId].field1 is not None:
                    self.scenes[scId].field1 = novel.scenes[scId].field1

                if novel.scenes[scId].field2 is not None:
                    self.scenes[scId].field2 = novel.scenes[scId].field2

                if novel.scenes[scId].field3 is not None:
                    self.scenes[scId].field3 = novel.scenes[scId].field3

                if novel.scenes[scId].field4 is not None:
                    self.scenes[scId].field4 = novel.scenes[scId].field4

                if novel.scenes[scId].tags is not None:
                    self.scenes[scId].tags = novel.scenes[scId].tags

                '''Do not modify these items yet:
                if novel.scenes[scId].isUnused is not None:
                    self.scenes[scId].isUnused = novel.chapters[chId].isUnused
                '''

        if novel.chapters != {}:

            for chId in novel.chapters:

                if novel.chapters[chId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].desc is not None:
                    self.chapters[chId].desc = novel.chapters[chId].desc

                '''Do not modify these items yet:
                if novel.chapters[chId].chLevel is not None:
                    self.chapters[chId].chLevel = novel.chapters[chId].chLevel

                if novel.chapters[chId].chType is not None:
                    self.chapters[chId].chType = novel.chapters[chId].chType

                if novel.chapters[chId].isUnused is not None:
                    self.chapters[chId].isUnused = novel.chapters[chId].isUnused

                if novel.chapters[chId].srtScenes != []:
                    self.chapters[chId].srtScenes = novel.chapters[chId].srtScenes
                '''

        # Overwrite the XML element tree items.

        root = self._tree.getroot()
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

                '''Do not modify these items yet:
                chp.find('Type').text = str(self.chapters[chId].chType)
                
                levelInfo = chp.find('SectionStart')
                
                if levelInfo is not None:
                    
                    if self.chapters[chId].chLevel == 0:
                         chp.remove(levelInfo)

                unusedMarker = chp.find('Unused')
                
                if unused is not None:
                    
                    if not self.chapters[chId].isUnused:
                         chp.remove(unusedMarker)
                '''

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
                '''
                if self.scenes[scId]._sceneContent is not None:
                    scn.find(
                        'SceneContent').text = self.scenes[scId]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId].letterCount)
                '''
                if self.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        newNotes = ET.SubElement(scn, 'Notes')
                        newNotes.text = self.scenes[scId].sceneNotes

                    else:
                        scn.find('Notes').text = self.scenes[scId].sceneNotes

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

                if self.scenes[scId].tags is not None:

                    if scn.find('Tags') is None:
                        newTags = ET.SubElement(scn, 'Tags')
                        newTags.text = ';'.join(self.scenes[scId].tags)

                    else:
                        scn.find('Tags').text = ';'.join(
                            self.scenes[scId].tags)

                '''Do not modify these items yet:
                unusedMarker = scn.find('Unused')
                
                if unused is not None:
                    
                    if not self.scenes[scId].isUnused:
                         scn.remove(unusedMarker)
                '''

        indent(root)
        self._tree = ET.ElementTree(root)

        try:
            self._tree.write(self._filePath)

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree.

        message = xml_postprocess(self._filePath, self._cdataTags)

        if message.startswith('ERROR'):
            return message

        if sceneCount > 0:
            info = str(sceneCount) + ' Scenes'

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
