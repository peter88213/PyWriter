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
        the chapter summary.

    chLevel : int
        a selector for the heading.
        0 = chapter level
        1 = section level (marked "begins a section")

    chType : int
        0 = chapter type (marked "Ch")
        1 = other type (marked "I")

    isUnused : bool
        the chapter is marked "unused".

    srtScenes : list 
        the chapter's scene IDs. The order of its elements 
        corresponds to the chapter's order of the scenes.
    """

    def __init__(self) -> None:
        self.title = None
        self.desc = None
        self.chLevel = None
        self.chType = None
        self.isUnused = None
        self.srtScenes = []
