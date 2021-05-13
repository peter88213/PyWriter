"""Provide a factory class for a yWriter 5 target object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw5_new_file import Yw5NewFile


class Yw5TargetFactory(FileFactory):
    """A factory class that instantiates a yw5 target file object."""

    def make_file_objects(self, sourcePath, suffix=None):
        """Instantiate a target object for conversion to yw5 format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: None
        - targetFile: a Yw5File instance, or None in case of error
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        if suffix is None:
            targetFile = Yw5NewFile(fileName + Yw5NewFile.EXTENSION)
            return 'SUCCESS', None, targetFile

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
