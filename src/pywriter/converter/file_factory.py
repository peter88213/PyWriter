"""Provide a base class for factories that instantiate conversion objects.

Converter-specific file factories inherit from this class.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class FileFactory:
    """Base class for conversion object factory classes.

    Public methods:
        make_file_objects(self, sourcePath, **kwargs) -- return conversion objects.

    This class emulates a "FileFactory" Interface.
    Instances can be used as stubs for factories instantiated at runtime.
    """

    def __init__(self, fileClasses=[]):
        """Write the parameter to a private instance variable.

        Private instance variables:
            fileClasses -- list of classes from which an instance can be returned.
        """
        self.fileClasses = fileClasses

    def make_file_objects(self, sourcePath, **kwargs):
        """A factory method stub.

        Positional arguments:
            sourcePath -- string; path to the source file to convert.

        Optional arguments:
            suffix -- string; an indicator for the target file type.

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
