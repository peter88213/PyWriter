""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import re
import xml.etree.ElementTree as ET


class PywProject():
    """ yWriter 7 project representation """

    class Chapter():
        """ yWriter 7 chapter representation """

        def __init__(self):
            self.title = ''
            self.type = ''
            self.scenes = []

    class Scene():
        """ yWriter 7 scene representation """

        def __init__(self):
            self.title = ''
            self.desc = ''
            self._wordCount = 0
            self._letterCount = 0
            self._sceneContent = ''

        @property
        def sceneContent(self):
            return(self._sceneContent)

        @sceneContent.setter
        def sceneContent(self, text):
            """ set sceneContent updating word count and letter count """
            self._sceneContent = text

            text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
            # Remove yw7 raw markup for word count
            wordList = text.split()
            self._wordCount = len(wordList)

            text = re.sub('\[.+?\]', '', self._sceneContent)
            # Remove yw7 raw markup for letter count
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            self._letterCount = len(text)

        def isEmpty(self):
            return(self.sceneContent == ' ')

    def __init__(self):
        """ Read data from yw7 project file """
        self.projectTitle = ''
        self.chapters = {}
        self.scenes = {}
        self.cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                          'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def read(self, yw7File):
        """ Read data from yw7 project file """
        try:
            # Empty scenes will crash the xml parser, so put a blank in them.
            with open(yw7File, 'r', encoding='utf-8') as f:
                xmlData = f.read()
        except(FileNotFoundError):
            sys.exit('\nERROR: "' + yw7File + '" not found.')

        if xmlData.count('<![CDATA[]]>'):
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')
            try:
                with open(yw7File, 'w', encoding='utf-8') as f:
                    f.write(xmlData)
            except(PermissionError):
                sys.exit('\nERROR: "' + yw7File + '" is write protected.')

        lines = xmlData.split('\n')

        for line in lines:
            # Complete list of tags requiring CDATA (if incomplete)
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
            if tag:
                if not (tag.group(1) in self.cdataTags):
                    self.cdataTags.append(tag.group(1))

        try:
            self.tree = ET.parse(yw7File)
            root = self.tree.getroot()
        except:
            sys.exit('\nERROR: Can not process "' + yw7File + '".')

        for prj in root.iter('PROJECT'):
            self.projectTitle = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapters[chID] = self.Chapter()
            self.chapters[chID].title = chp.find('Title').text
            self.chapters[chID].type = int(chp.find('Type').text)
            self.chapters[chID].scenes = []
            if chp.find('Scenes'):
                for scn in chp.find('Scenes').findall('ScID'):
                    self.chapters[chID].scenes.append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.scenes[scID] = self.Scene()
            self.scenes[scID].title = scn.find('Title').text
            if scn.find('Desc'):
                self.scenes[scID].desc = scn.find('Desc').text
            self.scenes[scID]._sceneContent = scn.find('SceneContent').text

    def write(self, yw7File):
        """ Write attributes to yw7 project file """
        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.projectTitle

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            chp.find('Title').text = self.chapters[chID].title
            chp.find('Type').text = str(self.chapters[chID].type)
            if chp.find('Scenes'):
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
                if scn.find('Desc'):
                    scn.find('Desc').text = self.scenes[scID].desc
                sceneCount = sceneCount + 1
            except(KeyError):
                return('\nERROR: Scene with ID:' + scID + ' is missing in input file - yWriter project not modified.')

        if sceneCount != len(self.scenes):
            return('\nERROR: Scenes total mismatch - yWriter project not modified.')

        try:
            self.tree.write(yw7File, encoding='utf-8')
        except(PermissionError):
            return('\nERROR: "' + yw7File + '" is write protected.')

        newXml = ['<?xml version="1.0" encoding="utf-8"?>\n']
        # try:
        with open(yw7File, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for tag in self.cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)
                newXml.append(line)
        # except:
        #    return('\nERROR: Can not read"' + yw7File + '".')
        try:
            with open(yw7File, 'w', encoding='utf-8') as f:
                f.writelines(newXml)
        except:
            return('\nERROR: Can not write"' + yw7File + '".')

        return('\nSUCCESS: ' + str(sceneCount) + ' Scenes written to "' + yw7File + '".')
