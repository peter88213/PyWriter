""" Library for yWriter7 file operations

"""

import re
import xml.etree.ElementTree as ET


def count_words(text):
    """ Required, because yWriter stores word counts. """
    text = re.sub('\[.+?\]|\.|\,| -', '', text)
    # Remove yw7 raw markup
    wordList = text.split()
    wordCount = len(wordList)
    return str(wordCount)


def count_letters(text):
    """ Required, because yWriter stores letter counts. """
    text = re.sub('\[.+?\]', '', text)
    # Remove yw7 raw markup
    letterCount = len(text)
    return str(letterCount)


class Project():
    """ yWriter 7 project data """

    def __init__(self, yw7File):
        """ Read data from yw7 project file """
        self.file = yw7File
        self.projectTitle = ''
        self.chapterTitles = {}
        self.sceneLists = {}
        self.sceneContents = {}
        self.sceneTitles = {}

        try:
            self.tree = ET.parse(self.file)
            root = self.tree.getroot()
        except(FileNotFoundError):
            return('\nERROR: "' + self.file + '" not found.')

        for prj in root.iter('PROJECT'):
            self.projectTitle = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chID = chp.find('ID').text
            self.chapterTitles[chID] = chp.find('Title').text
            self.sceneLists[chID] = []
            for scn in chp.find('Scenes').findall('ScID'):
                self.sceneLists[chID].append(scn.text)

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            self.sceneContents[scID] = scn.find('SceneContent').text
            self.sceneTitles[scID] = scn.find('Title').text

    def write_scene_contents(self, newContents):
        """ Write scene data to yw7 project file """
        self.sceneContents = newContents
        sceneCount = 0
        root = self.tree.getroot()

        for scn in root.iter('SCENE'):
            scID = scn.find('ID').text
            try:
                scn.find('SceneContent').text = self.sceneContents[scID]
                scn.find('WordCount').text = count_words(
                    self.sceneContents[scID])
                scn.find('LetterCount').text = count_letters(
                    self.sceneContents[scID])
            except:
                pass
            sceneCount = sceneCount + 1
        try:
            self.tree.write(self.file, encoding='utf-8')
        except(PermissionError):
            return('\nERROR: "' + self.file + '" is write protected.')

        return('\n' + str(sceneCount) + ' Scenes written to "' + self.file + '".')


if __name__ == '__main__':
    pass
