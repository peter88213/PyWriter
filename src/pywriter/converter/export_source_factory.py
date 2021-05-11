"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File

from pywriter.converter.file_factory import FileFactory


class ExportSourceFactory(FileFactory):
    """class for conversion object factory classes."""

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        This is a template method that calls primitive operations by case.

        """
        fileName, fileExtension = os.path.splitext(sourcePath)
        message = 'SUCCESS'

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath)

        elif fileExtension == Yw5File.EXTENSION:
            sourceFile = Yw5File(sourcePath)

        elif fileExtension == Yw6File.EXTENSION:
            sourceFile = Yw6File(sourcePath)

        else:
            sourceFile = None
            message = 'ERROR: Source file is not a yWriter project.'

        return message, sourceFile, None
