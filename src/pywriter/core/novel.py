"""Novel - represents the basic structure of an yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


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

    get_structure : str
        returns a string showing the order of chapters and scenes as 
        a tree. The result can be used to compare two Novel objects 
        by their structure.
    """

    def __init__(self):
        self.title = ''
        self.chapters = {}
        self.scenes = {}

    def get_structure(self) -> str:
        """Assemble a comparable structure tree. """

        text = ''
        for chID in self.chapters:
            text = text + 'ChID:' + str(chID) + '\n'
            for scID in self.chapters[chID].scenes:
                text = text + '  ScID:' + str(scID) + '\n'
        return(text)
