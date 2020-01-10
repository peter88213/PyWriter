"""yW7File - Class for yWriter 7 file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re
import xml.etree.ElementTree as ET
from pywriter.model.pywfile import PywFile
from pywriter.model.chapter import Chapter
from pywriter.model.scene import Scene


class Yw7File(PywFile):
    """yWriter 7 xml project file representation.

    # Attributes

    # Methods

    """
    _fileExtension = '.yw7'

    def __init__(self, filePath):
        PywFile.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def read(self) -> str:
        """Parse yw7 xml project file and store selected attributes. """

        try:
            # Read the file for preprocessing.
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        if '<![CDATA[]]>' in xmlData:
            # Empty scenes will crash the xml parser, so put a blank in them.
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')
            try:
                with open(self._filePath, 'w', encoding='utf-8') as f:
                    f.write(xmlData)

            except(PermissionError):
                return('ERROR: "' + self._filePath +
                       '" is write protected.')

        lines = xmlData.split('\n')
        for line in lines:
            # Complete list of tags requiring CDATA (if incomplete).
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        try:
            self.tree = ET.parse(self._filePath)
            # Open the file again and parse its xml structure.
            root = self.tree.getroot()

        except:
            return('ERROR: Can not process "' + self._filePath + '".')

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapters[chID] = Chapter()
            self.chapters[chID].title = chp.find('Title').text

            if chp.find('Desc') is not None:
                self.chapters[chID].desc = chp.find('Desc').text

            self.chapters[chID].type = int(chp.find('Type').text)
            self.chapters[chID].scenes = []

            if chp.find('Scenes') is not None:

                for scn in chp.find('Scenes').findall('ScID'):
                    self.chapters[chID].scenes.append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.scenes[scID] = Scene()
            self.scenes[scID].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scID].desc = scn.find('Desc').text

            self.scenes[scID]._sceneContent = scn.find('SceneContent').text

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write novel's attributes to yw7 project file. """

        if novel.title != '':
            self.title = novel.title

        if novel.scenes is not None:

            for scID in novel.scenes:

                if novel.scenes[scID].title != '':
                    self.scenes[scID].title = novel.scenes[scID].title

                if novel.scenes[scID].desc != '':
                    self.scenes[scID].desc = novel.scenes[scID].desc

                if novel.scenes[scID].sceneContent != '':
                    self.scenes[scID].sceneContent = novel.scenes[scID].sceneContent

        if novel.chapters is not None:

            for chID in novel.chapters:

                if novel.chapters[chID].title != '':
                    self.chapters[chID].title = novel.chapters[chID].title

                if novel.chapters[chID].desc != '':
                    self.chapters[chID].desc = novel.chapters[chID].desc

                if novel.chapters[chID].type is not None:
                    self.chapters[chID].type = novel.chapters[chID].type

                if novel.chapters[chID].scenes != []:
                    self.chapters[chID].scenes = []

                    for scID in novel.chapters[chID].scenes:
                        self.chapters[chID].scenes.append(scID)

        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            chp.find('Title').text = self.chapters[chID].title

            if self.chapters[chID].desc != '':
                if chp.find('Desc') is None:
                    newDesc = ET.SubElement(chp, 'Desc')
                    newDesc.text = self.chapters[chID].desc

                else:
                    chp.find('Desc').text = self.chapters[chID].desc

            chp.find('Type').text = str(self.chapters[chID].type)

            if chp.find('Scenes') is not None:
                i = 0
                for scn in chp.find('Scenes').findall('ScID'):
                    scn.text = self.chapters[chID].scenes[i]
                    i = i + 1

        for scn in root.iter('SCENE'):

            scID = scn.find('ID').text
            try:
                if self.scenes[scID].isEmpty():
                    scn.find('SceneContent').text = ''
                    scn.find('WordCount').text = '0'
                    scn.find('LetterCount').text = '0'

                else:
                    scn.find(
                        'SceneContent').text = self.scenes[scID]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scID]._wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scID]._letterCount)

                scn.find('Title').text = self.scenes[scID].title

                if self.scenes[scID].desc != '':
                    if scn.find('Desc') is None:
                        newDesc = ET.SubElement(scn, 'Desc')
                        newDesc.text = self.scenes[scID].desc

                    else:
                        scn.find('Desc').text = self.scenes[scID].desc

                sceneCount = sceneCount + 1

            except(KeyError):
                return('ERROR: Scene with ID:' + scID + ' is missing in input file - yWriter project not modified.')

        try:
            self.tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return('ERROR: "' + self._filePath + '" is write protected.')

        newXml = '<?xml version="1.0" encoding="utf-8"?>\n'
        with open(self._filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for tag in self._cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)
                newXml = newXml + line
        newXml = newXml.replace('\n \n', '\n')
        newXml = newXml.replace('[CDATA[ \n', '[CDATA[')
        newXml = newXml.replace('\n]]', ']]')
        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(newXml)

        except:
            return('ERROR: Can not write"' + self._filePath + '".')

        return('SUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self._filePath + '".')

    def is_locked(self) -> bool:

        if os.path.isfile(self._filePath + '.lock'):
            return(True)

        else:
            return(False)
