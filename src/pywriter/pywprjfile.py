""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from abc import abstractmethod
from pywriter.pywproject import PywProject


class PywPrjFile(PywProject):
    """ yWriter project file representation. """

    _fileExtension = ''

    def __init__(self, filePath):
        PywProject.__init__(self)
        self.filePath = filePath

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """ Accept only filenames with the right extension. """
        fileName = os.path.split(filePath)[1]
        fileName = fileName.lower()
        # Possibly Windows specific
        if fileName.count(self._fileExtension):
            self._filePath = filePath

    @abstractmethod
    def read(self):
        """ Read yWriter project data from a file. """
        pass

    @abstractmethod
    def write(self):
        """ Write yWriter project data to a file. """
        pass

    def file_is_present(self):
        """ Check whether the file is present. """
        if os.path.isfile(self._filePath):
            return(True)
        else:
            return(False)
