"""PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.proof.pypandoc import convert_file
from pywriter.proof.mdfile import MdFile


class OfficeFile(MdFile):

    _fileExtensions = ['docx', 'odt']

    def __init__(self, filePath):
        MdFile.__init__(self, 'temp.md')
        self._documentPath = None
        self.documentPath = filePath

    @property
    def documentPath(self):
        return(self._documentPath)

    @documentPath.setter
    def documentPath(self, pathToDoc):
        nameParts = pathToDoc.split('.')
        fileExt = nameParts[len(nameParts) - 1]
        if fileExt in self._fileExtensions:
            self._fileExtension = fileExt
            self._documentPath = pathToDoc

    def read(self):
        """Generate and read a temporary Markdown file. """

        if not os.path.isfile(self.documentPath):
            return('ERROR: "' + self.documentPath + '" not found.')

        convert_file(self.documentPath, 'markdown_strict', format=self._fileExtension,
                     outputfile=self.filePath, extra_args=['--wrap=none'])
        # Let pandoc read the document file and convert to markdown.

        message = MdFile.read(self)

        if message.startswith('ERROR'):
            return(message)

        return('SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".')

    def write(self, novel) -> str:
        """Write to a temporary Markdown file and convert it into an office document. """

        message = MdFile.write(self, novel)

        if message.startswith('ERROR'):
            return(message)

        try:
            os.remove(self.documentPath)

        except(FileNotFoundError):
            pass

        convert_file(self.filePath, self._fileExtension, format='markdown_strict',
                     outputfile=self.documentPath)
        # Let pandoc convert markdown and write to .document file.

        os.remove(self.filePath)

        if os.path.isfile(self.documentPath):
            return(message.replace(self.filePath, self.documentPath))

        else:
            return('ERROR: Could not create "' + self.documentPath + '".')

    def file_exists(self) -> bool:
        """Check whether the file specified by _filePath exists. """

        if os.path.isfile(self.documentPath):
            return(True)
        else:
            return(False)
