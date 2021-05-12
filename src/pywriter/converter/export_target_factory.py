"""Provide a factory class for any export target object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class ExportTargetFactory(FileFactory):
    """A factory class that instantiates an export target file object."""

    def __init__(self):
        self.expTargets = []
        # List of FileExport subclasses. To be set by the caller.

    def make_file_objects(self, sourcePath, suffix=None):
        """Instantiate a target object for conversion to any format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: None
        - targetFile: a FileExport subclass instance, or None in case of error 
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        for expTarget in self.expTargets:

            if expTarget.SUFFIX == suffix:
                targetFile = expTarget(fileName + suffix + expTarget.EXTENSION)
                return 'SUCCESS', None, targetFile

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
