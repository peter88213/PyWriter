"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File


class ExportSourceFactory:
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    """

    def __init__(self):
        self.expSources = [Yw7File, Yw6File, Yw5File]

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        for expSource in self.expSources:
            if expSource.EXTENSION == fileExtension:
                sourceFile = expSource(sourcePath)
                return 'SUCCESS', sourceFile, None

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
