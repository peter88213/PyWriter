"""An universal file factory. 

Instantiate the Novel subclass objects 
sourceFile and targetFile for file conversion.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from abc import ABC
from abc import abstractmethod


class FileFactory(ABC):
    """Abstract factory class that instantiates a source file object
    and a target file object for conversion.
    """

    @abstractmethod
    def get_file_objects(self, sourcePath, suffix=None):
        """Abstract method to be overwritten by subclasses.
        Return a tuple with three elements:
        * A message string starting with 'SUCCESS' or 'ERROR'
        * sourceFile: a Novel subclass instance
        * targetFile: a Novel subclass instance
        """
