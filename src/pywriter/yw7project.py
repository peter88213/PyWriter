""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import re
import xml.etree.ElementTree as ET
from pywriter.pywproject import PywProject


class Yw7Project(PywProject):
    """ yWriter project linked to an yw7 project file. """

    def __init__(self, fileName):
        PywProject.__init__(self)
        self.fileName = fileName

    def read(self):
        """ Read data from yw7 project file. """
        try:
            # Empty scenes will crash the xml parser, so put a blank in them.
            with open(self.fileName, 'r', encoding='utf-8') as f:
                xmlData = f.read()
        except(FileNotFoundError):
            sys.exit('\nERROR: "' + self.fileName + '" not found.')

        if xmlData.count('<![CDATA[]]>'):
            xmlData = xmlData.replace('<![CDATA[]]>', '<![CDATA[ ]]>')
            try:
                with open(self.fileName, 'w', encoding='utf-8') as f:
                    f.write(xmlData)
            except(PermissionError):
                sys.exit('\nERROR: "' + self.fileName +
                         '" is write protected.')

        lines = xmlData.split('\n')

        for line in lines:
            # Complete list of tags requiring CDATA (if incomplete)
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)
            if tag:
                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        try:
            self.tree = ET.parse(self.fileName)
            root = self.tree.getroot()
        except:
            sys.exit('\nERROR: Can not process "' + self.fileName + '".')

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text

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

    def write(self):
        """ Write attributes to yw7 project file. """
        sceneCount = 0
        root = self.tree.getroot()

        for prj in root.iter('PROJECT'):
            prj.find('Title').text = self.title

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
            self.tree.write(self.fileName, encoding='utf-8')
        except(PermissionError):
            return('\nERROR: "' + self.fileName + '" is write protected.')

        newXml = ['<?xml version="1.0" encoding="utf-8"?>\n']
        # try:
        with open(self.fileName, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                for tag in self._cdataTags:
                    line = re.sub('\<' + tag + '\>', '<' +
                                  tag + '><![CDATA[', line)
                    line = re.sub('\<\/' + tag + '\>',
                                  ']]></' + tag + '>', line)
                newXml.append(line)
        # except:
        #    return('\nERROR: Can not read"' + self.fileName + '".')
        try:
            with open(self.fileName, 'w', encoding='utf-8') as f:
                f.writelines(newXml)
        except:
            return('\nERROR: Can not write"' + self.fileName + '".')

        return('\nSUCCESS: ' + str(sceneCount) + ' Scenes written to "' + self.fileName + '".')
