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

    file = ''
    title = ''
    chpTitles = {}
    sceneList = {}
    scnContents = {}
    scnTitles = {}
    tree = None

    def get_title(self):
        """ Get the yw7 project title """
        return(self.title)

    def get_chapters(self):
        """ Get a list of chapter properties """
        return([self.chpTitles, self.sceneList])

    def get_scenes(self):
        """ Get a list of scene properties """
        return([self.scnTitles, self.scnContents])

    def __init__(self, yw7File):
        """ Read data from yw7 project file """
        self.file = yw7File
        self.scnContents = {}
        self.scnTitles = {}
        try:
            self.tree = ET.parse(self.file)
            root = self.tree.getroot()
        except(FileNotFoundError):
            return('\nERROR: "' + self.file + '" not found.')

        for prj in root.iter('PROJECT'):
            self.title = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chpID = chp.find('ID').text
            self.chpTitles[chpID] = chp.find('Title').text
            self.sceneList[chpID] = []
            for scn in chp.find('Scenes').findall('ScID'):
                self.sceneList[chpID].append(scn.text)

        for scn in root.iter('SCENE'):
            scnID = scn.find('ID').text
            self.scnContents[scnID] = scn.find('SceneContent').text
            self.scnTitles[scnID] = scn.find('Title').text

    def write_scenes(self, newScnContents):
        """ Write scene data to yw7 project file """
        sceneCount = 0
        root = self.tree.getroot()

        for scn in root.iter('SCENE'):
            scnID = scn.find('ID').text
            try:
                scn.find('SceneContent').text = newScnContents[scnID]
                scn.find('WordCount').text = count_words(
                    newScnContents[scnID])
                scn.find('LetterCount').text = count_letters(
                    newScnContents[scnID])
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
