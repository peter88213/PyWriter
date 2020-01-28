"""Scene - represents the basic structure of a scene in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


class Scene():
    """yWriter scene representation.

    # Attributes

    title : str
        the scene title.

    desc : str
        scene summary.

    sceneContent : str (property with setter)
        scene text with raw markup.

    wordCount : int 
        (to be updated by the sceneContent setter).

    letterCount : int 
        (to be updated by the sceneContent setter).

    isUnused : bool
        the scene is marked "unused".

    sceneNotes : str
        scene notes.

    tags : list
        list of scene tags.

    # Methods 

    isEmpty : bool
        True means: the scene is defined, but has no content.
    """

    def __init__(self):
        self.title = ''
        self.desc = ''
        self.wordCount = 0
        self.letterCount = 0
        self.isUnused = False
        self.tags = []
        self.sceneNotes = ''
        self._sceneContent = ''

    @property
    def sceneContent(self) -> str:
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text: str) -> None:
        """Set sceneContent updating word count and letter count. """

        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yw7 raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yw7 raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)

    def isEmpty(self) -> bool:
        """Check whether the scene has no content yet. """

        return self._sceneContent == ' '