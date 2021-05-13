"""Provide a factory class for any import source object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class ImportSourceFactory(FileFactory):
    """A factory class that instantiates a source file object for import or export."""

    def __init__(self, sourceClasses=[]):
        self.sourceClasses = sourceClasses

    def make_file_objects(self, sourcePath, suffix=None):
        """Instantiate a source object for conversion to a yWriter format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a YwFile subclass instance, or None in case of error
        - targetFile: None
        """

        for sourceClass in self.sourceClasses:

            if sourceClass.SUFFIX is not None:

                if sourcePath.endswith(sourceClass.SUFFIX + sourceClass.EXTENSION):
                    sourceFile = sourceClass(sourcePath)
                    return 'SUCCESS', sourceFile, None

        return 'ERROR: This document is not meant to be written back.', None, None
