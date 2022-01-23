"""Provide a generic class for yWriter project representation.

All classes representing specific file formats inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from urllib.parse import quote
from shutil import copy2
import os


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    Public methods: 
        convert_to_yw(text) -- Return text, converted from source format to yw7 markup.
        convert_from_yw(text) -- Return text, converted from yw7 markup to target format.

    Instance variables:
        title -- str; title
        desc -- str; description
        author -- str; author name
        fieldTitle1 -- str; field title 1
        fieldTitle2 -- str; field title 2
        fieldTitle3 -- str; field title 3
        fieldTitle4 -- str; field title 4
        chapters -- dict; key = chapter ID, value = Chapter instance.
        scenes -- dict; key = scene ID, value = Scene instance.
        srtChapters -- list of str; The novel's sorted chapter IDs. 
        locations -- dict; key = location ID, value = WorldElement instance.
        srtLocations -- list of str; The novel's sorted location IDs. 
        items -- dict; key = item ID, value = WorldElement instance.
        srtItems -- list of str; The novel's sorted item IDs. 
        characters -- dict; key = character ID, value = Character instance.
        srtCharacters -- list of str The novel's sorted character IDs.
        filePath -- str; path to the file represented by the class.   
    """

    DESCRIPTION = 'Novel'
    EXTENSION = None
    SUFFIX = None
    # To be extended by subclass methods.

    def __init__(self, filePath, **kwargs):
        """Define instance variables.

        Positional argument:
            filePath -- string; path to the file represented by the class.
        """
        self.title = None
        # str
        # xml: <PROJECT><Title>

        self.desc = None
        # str
        # xml: <PROJECT><Desc>

        self.author = None
        # str
        # xml: <PROJECT><AuthorName>

        self.fieldTitle1 = None
        # str
        # xml: <PROJECT><FieldTitle1>

        self.fieldTitle2 = None
        # str
        # xml: <PROJECT><FieldTitle2>

        self.fieldTitle3 = None
        # str
        # xml: <PROJECT><FieldTitle3>

        self.fieldTitle4 = None
        # str
        # xml: <PROJECT><FieldTitle4>

        self.chapters = {}
        # dict
        # xml: <CHAPTERS><CHAPTER><ID>
        # key = chapter ID, value = Chapter instance.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # dict
        # xml: <SCENES><SCENE><ID>
        # key = scene ID, value = Scene instance.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

        self.locations = {}
        # dict
        # xml: <LOCATIONS>
        # key = location ID, value = WorldElement instance.
        # The order of the elements does not matter.

        self.srtLocations = []
        # list of str
        # The novel's location IDs. The order of its elements
        # corresponds to the XML project file.

        self.items = {}
        # dict
        # xml: <ITEMS>
        # key = item ID, value = WorldElement instance.
        # The order of the elements does not matter.

        self.srtItems = []
        # list of str
        # The novel's item IDs. The order of its elements
        # corresponds to the XML project file.

        self.characters = {}
        # dict
        # xml: <CHARACTERS>
        # key = character ID, value = Character instance.
        # The order of the elements does not matter.

        self.srtCharacters = []
        # list of str
        # The novel's character IDs. The order of its elements
        # corresponds to the XML project file.

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a
        # supported type as specified by EXTENSION.

        self._projectName = None
        # str
        # URL-coded file name without suffix and extension.

        self._projectPath = None
        # str
        # URL-coded path to the project directory.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Setter for the filePath instance variable.        
        - Format the path string according to Python's requirements. 
        - Accept only filenames with the right suffix and extension.
        """

        if self.SUFFIX is not None:
            suffix = self.SUFFIX

        else:
            suffix = ''

        if filePath.lower().endswith((suffix + self.EXTENSION).lower()):
            self._filePath = filePath
            head, tail = os.path.split(os.path.realpath(filePath))
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(
                suffix + self.EXTENSION, ''))

    def convert_to_yw(self, text):
        """Return text, converted from source format to yw7 markup.
        This is a stub to be overridden by subclass methods.
        """
        return text

    def convert_from_yw(self, text):
        """Return text, converted from yw7 markup to target format.
        This is a stub to be overridden by subclass methods.
        """
        return text
