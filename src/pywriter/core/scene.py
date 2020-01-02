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
        scene description (summary).
    sceneContent : str (property with setter)
        scene text with raw markup.
    _wordCount : int 
        (to be updated by the sceneContent setter).
    _letterCount : int 
        (to be updated by the sceneContent setter).

    # Methods 

    isEmpty : bool
        True means: the scene is defined, but has no content.
    """

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
        """Set sceneContent updating word count and letter count. """

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

    def isEmpty(self) -> bool:
        """Check whether the scene has no content yet. """

        return(self._sceneContent == ' ')
