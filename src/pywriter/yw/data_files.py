"""Provide a class for yWriter XML data files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.data_writer import DataWriter
from pywriter.yw.data_postprocessor import DataPostprocessor


class DataFiles(Yw7File):
    """yWriter XML data files representation."""

    DESCRIPTION = 'yWriter XML data files'
    EXTENSION = '.xml'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        Extend the superclass constructor by changing
        the ywTreeBuilder strategy. 
        """
        Yw7File.__init__(self, filePath)

        self.ywTreeWriter = DataWriter()
        self.ywPostprocessor = DataPostprocessor()

    def merge(self, source):
        """Copy required attributes of the source object.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """
        self.characters = source.characters
        self.srtCharacters = source.srtCharacters
        self.locations = source.locations
        self.srtLocations = source.srtLocations
        self.items = source.items
        self.srtItems = source.srtItems
        return 'SUCCESS'
