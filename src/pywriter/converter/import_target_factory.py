"""Provide a factory class for any import target object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class ImportTargetFactory(FileFactory):
    """A factory class that instantiates an import target file object."""

    def make_file_objects(self, sourcePath, **kwargs):
        """Factory method.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: None
        - targetFile: a YwFile subclass instance, or None in case of error

        """
        fileName, fileExtension = os.path.splitext(sourcePath)
        sourceSuffix = kwargs['suffix']

        if sourceSuffix:
            ywPathBasis = fileName.split(sourceSuffix)[0]

        else:
            ywPathBasis = fileName

        # Look for an existing yWriter project to rewrite.

        for fileClass in self.fileClasses:

            if os.path.isfile(ywPathBasis + fileClass.EXTENSION):
                targetFile = fileClass(
                    ywPathBasis + fileClass.EXTENSION, **kwargs)
                return 'SUCCESS', None, targetFile

        return 'ERROR: No yWriter project to write.', None, None
