"""Provide a factory class for import source and target objects.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class ImportTargetFactory(FileFactory):
    """A factory class that instantiates a target file object for import."""

    def make_file_objects(self, sourcePath, sourceSuffix=''):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        """
        fileName, fileExtension = os.path.splitext(sourcePath)
        ywPathBasis = fileName.split(sourceSuffix)[0]

        # Look for an existing yWriter project to rewrite.

        for fileClass in self.fileClasses:

            if os.path.isfile(ywPathBasis + fileClass.EXTENSION):
                targetFile = fileClass(ywPathBasis + fileClass.EXTENSION)
                return 'SUCCESS', None, targetFile

        return 'ERROR: No yWriter project to write.', None, None
