"""Provide a class for yWriter chapter representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Chapter():
    """yWriter chapter representation.
    
    Public instance variables:
        title -- chapter title (may be the heading).
        desc -- chapter description in a single string.
        chLevel -- chapter level (part/chapter).
        oldType -- chapter type (Chapter/Other).
        chType -- chapter type yWriter 7.0.7.2+ (Normal/Notes/Todo).
        isUnused -- True, if the chapter is marked "Unused".
        suppressChapterTitle -- Suppress chapter title when exporting.
        isTrash -- True, if the chapter is the project's trash bin.
        suppressChapterBreak -- Suppress chapter break when exporting.
        srtScenes -- the chapter's sorted scene IDs.        
    """

    def __init__(self):
        """Initialize instance variables."""
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self.chLevel = None
        # int
        # xml: <SectionStart>
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.oldType = None
        # int
        # xml: <Type>
        # 0 = chapter type (marked "Chapter")
        # 1 = other type (marked "Other")
        # Applies to projects created by a yWriter version prior to 7.0.7.2.

        self.chType = None
        # int
        # xml: <ChapterType>
        # 0 = Normal
        # 1 = Notes
        # 2 = Todo
        # Applies to projects created by yWriter version 7.0.7.2+.

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.suppressChapterTitle = None
        # bool
        # xml: <Fields><Field_SuppressChapterTitle> 1
        # True: Chapter heading not to be displayed in written document.
        # False: Chapter heading to be displayed in written document.

        self.isTrash = None
        # bool
        # xml: <Fields><Field_IsTrash> 1
        # True: This chapter is the yw7 project's "trash bin".
        # False: This chapter is not a "trash bin".

        self.suppressChapterBreak = None
        # bool
        # xml: <Fields><Field_SuppressChapterBreak> 0

        self.srtScenes = []
        # list of str
        # xml: <Scenes><ScID>
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.

