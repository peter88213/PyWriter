"""Scene - represents the basic structure of a scene in yWriter.

Part of the PyWriter project.
Copyright (c) 2019, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


class Scene():
    """yWriter scene representation."""

    # Emulate an enumeration for the scene status

    STATUS = [None, 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done']

    def __init__(self):
        self.title = None
        # str

        self.desc = None
        # str

        self._sceneContent = None
        # str
        # Scene text with yW7 raw markup.

        self.wordCount = None
        # int
        # To be updated by the sceneContent setter

        self.letterCount = None
        # int
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool

        self.status = None
        # int

        self.tags = None
        # list of str

        self.sceneNotes = None
        # str

        self.field1 = None
        # str

        self.field2 = None
        # str

        self.field3 = None
        # str

        self.field4 = None
        # str

        self.appendToPrev = None
        # bool

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yWriter raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yWriter raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)
