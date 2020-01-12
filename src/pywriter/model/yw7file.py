"""yW7File - Class for yWriter 7 xml file operations and parsing.

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

    _cdataTags : list of str
        names of yw7 xml elements containing CDATA. 
        ElementTree.write omits CDATA tags, so they have to be 
        inserted afterwards. 

    # Methods

    read : str
        parse the yw7 xml file located at filePath, fetching the 
        Novel attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Arguments 
            novel : Novel
                the data to be written. 
        Open the yw7 xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.

    is_locked : bool
        tests whether a .lock file placed by yWriter exists.
    """

    _fileExtension = '.yw7'
    # overwrites PywFile._fileExtension

    def __init__(self, filePath):
        PywFile.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def read(self) -> str:
        """Parse yw7 xml project file and store selected attributes. """

        # Preprocess the xml file:
        # Empty scenes will crash the xml parser, so put a blank in them.

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return('ERROR: "' + self._filePath + '" not found.')

        if '<![CDATA[]]>' in xmlData:
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')

            try:
                with open(self._filePath, 'w', encoding='utf-8') as f:
                    f.write(xmlData)

            except(PermissionError):
                return('ERROR: "' + self._filePath +
                       '" is write protected.')

        # Complete list of tags requiring CDATA (if incomplete).

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
            return('ERROR: Can not process "' + self._filePath + '".')

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text
            self.desc = prj.find('Desc').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            self.chapters[chId].type = int(chp.find('Type').text)
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

            self.scenes[scId].sceneContent = scn.find('SceneContent').text

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write novel's attributes to yw7 project file. """

        # Copy the novel's attributes to write

        if novel.title != '':
            self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:

            for scId in novel.scenes:

                if novel.scenes[scId].title != '':
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].desc != '':
                    self.scenes[scId].desc = novel.scenes[scId].desc

                if novel.scenes[scId].sceneContent != '':
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

        if novel.chapters is not None:

            for chId in novel.chapters:

                if novel.chapters[chId].title != '':
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].desc != '':
                    self.chapters[chId].desc = novel.chapters[chId].desc

                if novel.chapters[chId].type is not None:
                    self.chapters[chId].type = novel.chapters[chId].type

                if novel.chapters[chId].srtScenes != []:
                    self.chapters[chId].srtScenes = novel.chapters[chId]

        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            chp.find('Title').text = self.chapters[chId].title

            if self.chapters[chId].desc != '':
                if chp.find('Desc') is None:
                    newDesc = ET.SubElement(chp, 'Desc')
                    newDesc.text = self.chapters[chId].desc

                else:
                    chp.find('Desc').text = self.chapters[chId].desc

            chp.find('Type').text = str(self.chapters[chId].type)

        for scn in root.iter('SCENE'):

            scId = scn.find('ID').text
            try:
                if self.scenes[scId].isEmpty():
                    scn.find('SceneContent').text = ''
                    scn.find('WordCount').text = '0'
                    scn.find('LetterCount').text = '0'

                else:
                    scn.find(
                        'SceneContent').text = self.scenes[scId]._sceneContent
                    scn.find('WordCount').text = str(
                        self.scenes[scId]._wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId]._letterCount)

                scn.find('Title').text = self.scenes[scId].title

                if self.scenes[scId].desc != '':
                    if scn.find('Desc') is None:
                        newDesc = ET.SubElement(scn, 'Desc')
                        newDesc.text = self.scenes[scId].desc

                    else:
                        scn.find('Desc').text = self.scenes[scId].desc

                sceneCount = sceneCount + 1

            except(KeyError):
                return('ERROR: Scene with ID:' + scId + ' is missing in input file - yWriter project not modified.')

        try:
            self.tree.write(self._filePath, encoding='utf-8')

        except(PermissionError):
            return('ERROR: "' + self._filePath + '" is write protected.')

        # Postprocess the xml file created by ElementTree:
        # Put a header on top and insert the missing CDATA tags.

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
