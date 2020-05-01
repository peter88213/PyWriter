"""Chapter - represents the basic structure of a chapter in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Chapter():
    """yWriter chapter representation."""

    def __init__(self):
        self.title = None
        # str

        self.desc = None
        # str

        self.chLevel = None
        # int
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.chType = None
        # int
        # 0 = chapter type (marked "Chapter")
        # 1 = other type (marked "Other")

        self.isUnused = None
        # bool

        self.suppressChapterTitle = None
        # bool
        # True: Remove 'Chapter ' from the chapter title upon import.
        # False: Do not modify the chapter title.

        self.srtScenes = []
        # list of str
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.

    def get_title(self):
        """Fix auto-chapter titles for non-English """
        text = self.title

        if self.suppressChapterTitle:
            text = text.replace('Chapter ', '')

        return text
