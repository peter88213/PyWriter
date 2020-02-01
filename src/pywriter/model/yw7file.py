"""yW7File - Class for yWriter 7 xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
import xml.etree.ElementTree as ET

from pywriter.model.novel import Novel
from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene
from pywriter.model.xform import *


class Yw7File(PywFile):
    """yWriter 7 xml project file representation.
    """

    _FILE_EXTENSION = '.yw7'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath: str) -> None:
        PywFile.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']
        # Names of yw7 xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    def read(self) -> str:
        """Parse the yw7 xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Complete list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)

            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        # Open the file again and let ElementTree parse its xml structure.

        try:
            self.tree = ET.parse(self._filePath)
            root = self.tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text
            if prj.find('Desc') is not None:
                self.summary = prj.find('Desc').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].summary = chp.find('Desc').text

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
                self.scenes[scId].summary = scn.find('Desc').text

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

            if scn.find('Tags') is not None:
                self.scenes[scId].tags = scn.find('Tags').text.split(';')

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Open the yw7 xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the novel's attributes to write

        if novel.title is not None:
            self.title = novel.title

        if novel.summary is not None:
            self.summary = novel.summary

        '''Do not modify these items yet:
        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters
        '''

        if novel.scenes is not None:

            for scId in novel.scenes:

                if novel.scenes[scId].title is not None:
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].summary is not None:
                    self.scenes[scId].summary = novel.scenes[scId].summary

                if novel.scenes[scId].sceneNotes is not None:
                    self.scenes[scId].sceneNotes = novel.scenes[scId].sceneNotes

                if novel.scenes[scId].tags is not None:
                    self.scenes[scId].tags = novel.scenes[scId].tags

                if novel.scenes[scId].sceneContent is not None:
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

                '''Do not modify these items yet:
                if novel.scenes[scId].isUnused is not None:
                    self.scenes[scId].isUnused = novel.chapters[chId].isUnused
                '''

        if novel.chapters is not None:

            for chId in novel.chapters:

                if novel.chapters[chId].title is not None:
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].summary is not None:
                    self.chapters[chId].summary = novel.chapters[chId].summary

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

        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

            if self.summary is not None:

                if prj.find('Desc') is None:
                    newDesc = ET.SubElement(prj, 'Desc')
                    newDesc.text = self.summary

                else:
                    prj.find('Desc').text = self.summary

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in self.chapters:
                chp.find('Title').text = self.chapters[chId].title

                if self.chapters[chId].summary is not None:

                    if chp.find('Desc') is None:
                        newDesc = ET.SubElement(chp, 'Desc')
                        newDesc.text = self.chapters[chId].summary

                    else:
                        chp.find('Desc').text = self.chapters[chId].summary

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

                if self.scenes[scId].summary is not None:

                    if scn.find('Desc') is None:
                        newDesc = ET.SubElement(scn, 'Desc')
                        newDesc.text = self.scenes[scId].summary

                    else:
                        scn.find('Desc').text = self.scenes[scId].summary

                if self.scenes[scId]._sceneContent is not None:
                    scn.find(
                        'SceneContent').text = self.scenes[scId]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId].letterCount)

                if self.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        newNotes = ET.SubElement(scn, 'Notes')
                        newNotes.text = self.scenes[scId].sceneNotes

                    else:
                        scn.find('Notes').text = self.scenes[scId].sceneNotes

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

                sceneCount = sceneCount + 1

        indent(root)
        tree = ET.ElementTree(root)

        try:
            self.tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree
        message = cdata(self._filePath, self._cdataTags)

        if 'ERROR' in message:
            return message

        return 'SUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self._filePath + '".'

    def is_locked(self) -> bool:
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False
