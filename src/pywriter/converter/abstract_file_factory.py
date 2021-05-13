"""Provide an abstract factory for conversion object instantiation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.file_factory import FileFactory
from pywriter.converter.export_source_factory import ExportSourceFactory
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.converter.import_source_factory import ImportSourceFactory
from pywriter.converter.import_target_factory import ImportTargetFactory


class AbstractFileFactory(FileFactory):
    """Abstract factory for conversion objects."""

    EXPORT_SOURCE_CLASSES = []
    EXPORT_TARGET_CLASSES = []
    IMPORT_SOURCE_CLASSES = []
    IMPORT_TARGET_CLASSES = []

    def __init__(self):
        """Set the instance variables for the abstract factory:

        exportSourceFactory (default: ExportSourceFactory)
        exportTargetFactory (default: ExportTargetFactory)
        importSourceFactory (default: ImportSourceFactory)
        importTargetFactory (default: ImportTargetFactory)
        """
        self.exportSourceFactory = ExportSourceFactory(
            self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(
            self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(
            self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(
            self.IMPORT_TARGET_CLASSES)

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

            if message.startswith('ERROR'):
                return message, None, None

        else:
            # The source file is not a yWriter project.

            message, sourceFile, dummy = self.importSourceFactory.make_file_objects(
                sourcePath)

            if message.startswith('SUCCESS'):
                message, dummy, targetFile = self.importTargetFactory.make_file_objects(
                    sourcePath, sourceFile.SUFFIX)

            if message.startswith('ERROR'):
                return message, None, None

        return message, sourceFile, targetFile
