"""Provide a factory class for any export source object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class ExportSourceFactory(FileFactory):
    """A factory class that instantiates an export source file object."""

    def make_file_objects(self, sourcePath, **kwargs):
        """Instantiate a source object for conversion from a yWriter format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a YwFile subclass instance, or None in case of error
        - targetFile: None
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        for fileClass in self.fileClasses:

            if fileClass.EXTENSION == fileExtension:
                sourceFile = fileClass(sourcePath, **kwargs)
                return 'SUCCESS', sourceFile, None

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
