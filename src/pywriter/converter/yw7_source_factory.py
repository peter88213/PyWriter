"""Provide a factory class for a yWriter 7 source object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory
from pywriter.yw.yw7_file import Yw7File


class Yw7SourceFactory(FileFactory):
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    """

    def make_file_objects(self, sourcePath, suffix=None):
        """Instantiate a source object for conversion from yw7 format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Yw7File instance, or None in case of error
        - targetFile: None
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        if Yw7File.EXTENSION == fileExtension:
            sourceFile = Yw7File(sourcePath)
            return 'SUCCESS', sourceFile, None

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
