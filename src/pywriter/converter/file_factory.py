"""Provide an interface emulation for conversion object factory classes.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class FileFactory:
    """Base class for conversion object factory classes.

    This class emulates a "FileFactory" Interface.
    Instances can be used as stubs for factories instantiated at runtime.
    """

    def make_file_objects(self, sourcePath, suffix=None):
        """A factory method stub.

        Return a tuple with three elements:
        - A message string starting with 'ERROR'
        - sourceFile: None
        - targetFile: None

        Factory method to be overwritten by subclasses.
        Subclasses return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        """
        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
