"""Chapter - represents the basic structure of a chapter in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Chapter():
    """yWriter chapter representation.

    # Attributes

    title : str
        the chapter title.
    desc : str
        the chapter description (summary).
    type : int
        a selector for the chapter's level.
    scenes : list 
        the chapter's scene IDs. The order of its elements 
        corresponds to the chapter's order of the scenes.
    """

    def __init__(self):
        self.title = ''
        self.desc = ''
        self.type = ''
        self.scenes = []
