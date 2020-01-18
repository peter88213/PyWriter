"""Collection - represents the basic structure of a collection of yWriter projects.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os


class Collection():
    """yWriter project representation. 

    # Attributes

    desc : str
        the novel summary.

    books : dict
        key = scene ID, value = Book object.
        The order of the elements does not matter.

    srtSeries : list 
        the collection's series IDs.

    # Properties

    filePath : str (property with setter)
        Path to the file.
        The setter only accepts files of a supported type as specified 
        by _fileExtension. 

    # Methods 

    read : str
        parse the pwc xml file located at filePath, fetching the 
        Collection attributes.
        Return a message beginning with SUCCESS or ERROR. 

    write : str
        Open the pwc xml file located at filePath and replace a set 
        of items by the novel attributes not being None.
        Return a message beginning with SUCCESS or ERROR.

    file_exists() : bool
        True means: the file specified by filePath exists. 
    """

    _fileExtension = 'pwc'

    def __init__(self, filePath):
        self.books = {}
        self.srtSeries = []
        self._filePath = None
        self.filePath = filePath

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._fileExtension):
            self._filePath = filePath

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self._filePath):
            return(True)

        else:
            return(False)
