"""PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.technical.pypandoc import convert_file
from pywriter.model.mdfile import MdFile


class OfficeFile(MdFile):

    _fileExtensions = ['docx', 'odt']

    def __init__(self, filePath):
        MdFile.__init__(self, 'temp.md')
        self._filePath = None
        self.filePath = filePath
        self._tempFile = 'temp.md'

    @property
    def filePath(self):
        return(self._filePath)

    @filePath.setter
    def filePath(self, documentPath):
        nameParts = documentPath.split('.')
        fileExt = nameParts[len(nameParts) - 1]
        if fileExt in self._fileExtensions:
            self._fileExtension = fileExt
            self._filePath = documentPath

    def read(self):
        """Generate and read a temporary Markdown file. """

        if not os.path.isfile(self.filePath):
            return('ERROR: "' + self.filePath + '" not found.')

        convert_file(self.filePath, 'markdown_strict', format=self._fileExtension,
                     outputfile=self._tempFile, extra_args=['--wrap=none'])
        # Let pandoc read the document file and convert to markdown.

        documentPath = self._filePath
        self._filePath = self._tempFile
        message = MdFile.read(self)
        self._filePath = documentPath
        os.remove(self._tempFile)

        if message.startswith('ERROR'):
            return(message)

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write to a temporary Markdown file and convert it into an office document. """

        documentPath = self._filePath
        self._filePath = self._tempFile
        message = MdFile.write(self, novel)
        self._filePath = documentPath

        if message.startswith('ERROR'):
            return(message)

        try:
            os.remove(self.filePath)

        except(FileNotFoundError):
            pass

        convert_file(self._tempFile, self._fileExtension, format='markdown_strict',
                     outputfile=self.filePath)
        # Let pandoc convert markdown and write to .document file.

        os.remove(self._tempFile)

        if os.path.isfile(self.filePath):
            return(message.replace(self._tempFile, self.filePath))

        else:
            return('ERROR: Could not create "' + self.filePath + '".')

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self.filePath):
            return(True)
        else:
            return(False)
