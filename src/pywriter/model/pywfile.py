"""PywFile - abstract base class for files storing an yWriter structure.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from abc import abstractmethod, ABC

from pywriter.model.novel import Novel


class PywFile(Novel, ABC):
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    # Properties

    filePath : str (property with setter)
        Path to the file. The setter only accepts files of a 
        supported type as specified by _FILE_EXTENSION. 
    """

    _FILE_EXTENSION = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath: str) -> None:
        Novel.__init__(self)
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self) -> str:
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str) -> None:
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    @abstractmethod
    def read(self) -> None:
        """Parse the file and store selected properties.
        To be overwritten by file format specific subclasses.
        """

    @abstractmethod
    def write(self, novel: Novel):
        """Write selected novel properties to the file.
        To be overwritten by file format specific subclasses.
        """

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self._filePath):
            return True

        else:
            return False
