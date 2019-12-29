""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from abc import ABC


class PywProject(ABC):
    """ yWriter project representation. """

    class Chapter():
        """ yWriter chapter representation. """

        def __init__(self):
            self.title = ''
            self.type = ''
            self.scenes = []

    class Scene():
        """ yWriter scene representation. """

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
            """ set sceneContent updating word count and letter count. """
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
            return(self._sceneContent == ' ')

    def __init__(self):
        """ Read data from yw7 project file. """
        self.title = ''
        self.chapters = {}
        self.scenes = {}
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']

    def get_text(self):
        """ Assemble all scenes in the right order as plain text. """

        text = ''
        for chID in self.chapters:
            text = text + '\n\n' + self.chapters[chID].title + '\n\n'
            for scID in self.chapters[chID].scenes:
                try:
                    text = text + self.scenes[scID].sceneContent + '\n'
                except(TypeError):
                    text = text + '\n'
        text = re.sub('\[.+?\]', '', text)
        return(text)

    def getStructure(self):
        """ Assemble a comparable structure tree. """

        text = ''
        for chID in self.chapters:
            text = text + 'ChID:' + str(chID) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '  ScID:' + str(scID) + '\n'
        return(text)
