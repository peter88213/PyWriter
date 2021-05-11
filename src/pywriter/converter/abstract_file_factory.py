"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class AbstractFileFactory(FileFactory):
    """Abstract factory for conversion objects."""

    def __init__(self):
        self.exportSourceFactory = FileFactory()
        self.exportTargetFactory = FileFactory()
        self.importObjectsFactory = FileFactory()

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        This is a template method that calls primitive operations by case.

        """
        message, sourceFile, dummy = self.exportSourceFactory.make_file_objects(
            sourcePath)

        if message.startswith('SUCCESS'):
            # The source file is a yWriter project.

            message, dummy, targetFile = self.exportTargetFactory.make_file_objects(
                sourcePath, suffix)

        else:
            # The source file is not a yWriter project.

            message, sourceFile, targetFile = self.importObjectsFactory.make_file_objects(
                sourcePath)

        return message, sourceFile, targetFile
