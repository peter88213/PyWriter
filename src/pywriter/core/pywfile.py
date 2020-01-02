"""PywFile - abstract base class for files storing an yWriter structure.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from abc import abstractmethod, ABC
from pywriter.core.novel import Novel


class PywFile(Novel, ABC):
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    # Properties

    filePath : str (property with setter)
        Path to the file.

    # Methods

    read()
        Abstract method for opening and parsing the file.
    write() : str
        write selected contents to the file and return a message.
    file_exists() : bool
        True means: the file specified by filePath exists. 
    """

    _fileExtension = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
        Novel.__init__(self)
        self.filePath = filePath

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        fileName = os.path.split(filePath)[1]
        fileName = fileName.lower()
        if fileName.count(self._fileExtension):
            self._filePath = filePath

    @abstractmethod
    def read(self):
        """Read yWriter project data from a file and parse it. """

        # To be overwritten by file format specific subclasses.
        pass

    def write(self) -> str:
        """ Write yWriter project data to a file. """

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(self.get_text())
                # get_text() is to be overwritten
                # by file format specific subclasses.
        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes written to "' + self._filePath + '".')

    def file_exists(self) -> bool:
        """ Check whether the file specified by _filePath exists. """

        if os.path.isfile(self._filePath):
            return(True)
        else:
            return(False)
