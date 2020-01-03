"""Novel - represents the basic structure of an yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re


class Novel():
    """yWriter project representation. 

    # Attributes

    title : str
        the novel's title.
    chapters : dict 
        key = chapter ID, value = Chapter object.
        The order of the elements corresponds to the novel's order 
        of the chapters.
    scenes : dict
        key = scene ID, value = Scene object.
        The order of the elements does not matter (the novel's 
        order of the scenes is defined by the order of the chapters 
        and the order of the scenes within the chapters)

    # Methods 

    get_text : str
        parses the "chapters" tree and returns all scene contents 
        assembled to a single string. This method is to be overwritten 
        by file format specific subclasses.

    get_structure : str
        returns a string showing the order of chapters and scenes as 
        a tree. The result can be used to compare two Novel objects 
        by their structure.
    """

    def __init__(self):
        self.title = ''
        self.chapters = {}
        self.scenes = {}

    def get_text(self) -> str:
        """Assemble all scenes in the right order as plain text. """

        # To be overwritten by file format specific subclasses.
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

    def get_structure(self) -> str:
        """Assemble a comparable structure tree. """

        text = ''
        for chID in self.chapters:
            text = text + 'ChID:' + str(chID) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '  ScID:' + str(scID) + '\n'
        return(text)
