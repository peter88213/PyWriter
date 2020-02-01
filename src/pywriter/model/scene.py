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
        The scene title.

    summary : str
        The scene summary.

    sceneContent : str (property with setter)
        Scene text with raw markup.

    wordCount : int 
        (to be updated by the sceneContent setter).

    letterCount : int 
        (to be updated by the sceneContent setter).

    isUnused : bool
        The scene is marked "unused".

    sceneNotes : str
        Scene notes.

    tags : list
        List of scene tags.
    """

    def __init__(self):
        self.title = None
        self.summary = None
        self.wordCount = None
        self.letterCount = None
        self.isUnused = None
        self.tags = None
        self.sceneNotes = None
        self._sceneContent = None

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
