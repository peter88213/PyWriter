"""Novel - represents the basic structure of an yWriter project.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from urllib.parse import quote
import os


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).
    """

    DESCRIPTION = 'Novel'
    EXTENSION = None
    SUFFIX = None
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
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
        # key = chapter ID, value = Chapter object.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # dict
        # xml: <SCENES><SCENE><ID>
        # key = scene ID, value = Scene object.
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
        # key = location ID, value = Object.
        # The order of the elements does not matter.

        self.srtLocations = []
        # list of str
        # The novel's location IDs. The order of its elements
        # corresponds to the XML project file.

        self.items = {}
        # dict
        # xml: <ITEMS>
        # key = item ID, value = Object.
        # The order of the elements does not matter.

        self.srtItems = []
        # list of str
        # The novel's item IDs. The order of its elements
        # corresponds to the XML project file.

        self.characters = {}
        # dict
        # xml: <CHARACTERS>
        # key = character ID, value = Character object.
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
        """Accept only filenames with the right extension. """

        if self.SUFFIX is not None:
            suffix = self.SUFFIX

        else:
            suffix = ''

        if filePath.lower().endswith(suffix + self.EXTENSION):
            self._filePath = filePath
            head, tail = os.path.split(os.path.realpath(filePath))
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(
                suffix + self.EXTENSION, ''))

    def read(self):
        """Parse the file and store selected properties.
        To be overwritten by file format specific subclasses.
        """
        return 'ERROR: read method is not implemented.'

    def merge(self, novel):
        """Copy required attributes of the novel object.
        To be overwritten by file format specific subclasses.
        """
        return 'ERROR: merge method is not implemented.'

    def write(self):
        """Write selected properties to the file.
        To be overwritten by file format specific subclasses.
        """
        return 'ERROR: write method is not implemented.'

    def convert_to_yw(self, text):
        """Convert source format to yw7 markup.
        To be overwritten by file format specific subclasses.
        """
        return text

    def convert_from_yw(self, text):
        """Convert yw7 markup to target format.
        To be overwritten by file format specific subclasses.
        """
        return text

    def file_exists(self):
        """Check whether the file specified by filePath exists. """
        if os.path.isfile(self.filePath):
            return True

        else:
            return False
