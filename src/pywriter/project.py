""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import re
import xml.etree.ElementTree as ET


class PywProject():
    """ yWriter 7 project data """

    def __init__(self, yw7File):
        """ Read data from yw7 project file """
        self.file = yw7File
        self.projectTitle = ''
        self.chapterTitles = {}
        self.chapterTypes = {}
        self.sceneLists = {}
        self.sceneContents = {}
        self.sceneTitles = {}
        self.sceneDescriptions = {}

        self.cdataTags = []

        try:
            # Empty scenes will crash the xml parser, so put a blank in them.
            with open(self.file, 'r', encoding='utf-8') as f:
                xmlData = f.read()
        except(FileNotFoundError):
            sys.exit('\nERROR: "' + self.file + '" not found.')

        if xmlData.count('<![CDATA[]]>'):
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')
            try:
                with open(self.file, 'w', encoding='utf-8') as f:
                    f.write(xmlData)
            except(PermissionError):
                sys.exit('\nERROR: "' + self.file + '" is write protected.')

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
            if tag:
                if not (tag.group(1) in self.cdataTags):
                    self.cdataTags.append(tag.group(1))
        try:
            self.tree = ET.parse(self.file)
            root = self.tree.getroot()
        except:
            sys.exit('\nERROR: Can not process "' + self.file + '".')

        for prj in root.iter('PROJECT'):
            self.projectTitle = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapterTitles[chID] = chp.find('Title').text
            self.chapterTypes[chID] = int(chp.find('Type').text)
            self.sceneLists[chID] = []
            if chp.find('Scenes'):
                for scn in chp.find('Scenes').findall('ScID'):
                    self.sceneLists[chID].append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.sceneContents[scID] = scn.find('SceneContent').text
            self.sceneTitles[scID] = scn.find('Title').text
            if scn.find('Desc'):
                self.sceneDescriptions[scID] = scn.find('Desc').text

    def write_scene_contents(self, newContents):
        """ Write scene data to yw7 project file """
        if len(newContents) != len(self.sceneContents):
            return('\nERROR: Scenes total mismatch - yWriter project not modified.')

        sceneCount = 0
        root = self.tree.getroot()

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            try:
                if newContents[scID] == ' ':
                    scn.find('SceneContent').text = ''
                    scn.find('WordCount').text = '0'
                    scn.find('LetterCount').text = '0'
                else:
                    scn.find('SceneContent').text = newContents[scID]
                    scn.find('WordCount').text = self.count_words(
                        newContents[scID])
                    scn.find('LetterCount').text = self.count_letters(
                        newContents[scID])
                sceneCount = sceneCount + 1
            except(KeyError):
                return('\nERROR: Scene with ID:' + scID + ' is missing in input file - yWriter project not modified.')

        self.sceneContents = newContents
        try:
            self.tree.write(self.file, encoding='utf-8')
        except(PermissionError):
            return('\nERROR: "' + self.file + '" is write protected.')

        newXml = ['<?xml version="1.0" encoding="utf-8"?>\n']
        # try:
        with open(self.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for tag in self.cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)
                newXml.append(line)
        # except:
        #    return('\nERROR: Can not read"' + self.file + '".')
        try:
            with open(self.file, 'w', encoding='utf-8') as f:
                f.writelines(newXml)
        except:
            return('\nERROR: Can not write"' + self.file + '".')

        return('\nSUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self.file + '".')

    def count_words(self, text):
        """ Required, because yWriter stores word counts. """
        text = re.sub('\[.+?\]|\.|\,| -', '', text)
        # Remove yw7 raw markup
        wordList = text.split()
        wordCount = len(wordList)
        return str(wordCount)

    def count_letters(self, text):
        """ Required, because yWriter stores letter counts. """
        text = re.sub('\[.+?\]', '', text)
        # Remove yw7 raw markup
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        letterCount = len(text)
        return str(letterCount)
