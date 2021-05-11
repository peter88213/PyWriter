"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File


class FileFactory:
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    """

    def make_file_objects(self, sourcePath, suffix=None):
        """Return source and target objects for conversion, and a message.

        Factory method to be overwritten by subclasses.
        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance

        This is a template method that calls primitive operations by case.

        """
        sourceFile = self.make_export_source(sourcePath)

        if sourceFile is not None:
            # The source file is a yWriter project.

            targetFile = self.make_export_target(sourcePath, suffix)

            if targetFile is None:
                return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None

            else:
                return 'SUCCESS', sourceFile, targetFile

        else:
            # The source file is not a yWriter project.

            return self.make_import_objects(self, sourcePath)

    def make_export_source(self, sourcePath):
        """

        This is a primitive operation of the make_file_objects() template method.

        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath)

        elif fileExtension == Yw5File.EXTENSION:
            sourceFile = Yw5File(sourcePath)

        elif fileExtension == Yw6File.EXTENSION:
            sourceFile = Yw6File(sourcePath)

        else:
            sourceFile = None

        return sourceFile

    def make_export_target(self, sourcePath, suffix):
        """

        This is a primitive operation of the make_file_objects() template method.

        """
        return None

    def make_import_objects(self, sourcePath):
        """Factory method.
        Return a tuple with three elements:
        * A message string starting with 'SUCCESS' or 'ERROR'
        * sourceFile: a Novel subclass instance
        * targetFile: a Novel subclass instance

        This is a primitive operation of the make_file_objects() template method.

        """
        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
