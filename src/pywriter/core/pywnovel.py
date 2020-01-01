"""PywNovel - The PyWriter base class

This class represents the data strcture of an yWriter 7 project.

# Properties

The parts of yWriter's project structure mapped in the PywNovel class: 

PyWProject
    |
    +--title
    +--chapters = {chID1:Chapter, chID2:Chapter, ... chIDm:Chapter} (ordered dictionary)
    |                        |
    |                        +--title (used for chapter headings)
    |                        +--desc (to be used for synopsis)
    |                        +--type (used as a selector for the chapter's level)
    |                        +--scenes = [scID1, scID2, ... scIDn] (ordered list)
    |
    +--scenes = {scID1:Scene, scID2:Scene, scIDn:Scene} (dictionary; order doesn't matter)
                        |
                        +--title (used for html comments shown in Open/LibreOffice)
                        +--desc (to be used for synopsis)
                        +--sceneContent (property with setter)
                        +--_wordCount (to be updated by the sceneContent setter)
                        +--_letterCount (to be updated by the sceneContent setter)
# Methods 

- get_text      parses the "chapters" tree and assembles all scene contents to a raw text.
                This method is to be overwritten by file format specific subclasses.
                
- get_structure returns a string showing the order of chapters and scenes as a tree.
                The result can be used to compare two PywNovel objects.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re


class PywNovel():
    """ yWriter project representation. """

    class Chapter():
        """ yWriter chapter representation. """

        def __init__(self):
            self.title = ''
            self.desc = ''
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

    def get_structure(self):
        """ Assemble a comparable structure tree. """

        text = ''
        for chID in self.chapters:
            text = text + 'ChID:' + str(chID) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '  ScID:' + str(scID) + '\n'
        return(text)
