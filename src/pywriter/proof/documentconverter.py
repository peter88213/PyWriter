"""Import and export ywriter7 scenes for proofing.

Proof reading Office document

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.proof.mdconverter import MdConverter
from pywriter.proof.pypandoc import convert_file


class DocumentConverter(MdConverter):

    _fileExtensions = ['docx', 'odt']

    def __init__(self, yw7Path, pathToDoc):
        self.mdPath = 'temp.md'
        MdConverter.__init__(self, yw7Path, self.mdPath)
        self.documentPath = pathToDoc

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

    def yw7_to_document(self):
        """Export to document """

        message = self.yw7_to_md()
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(self.documentPath):
            self.confirm_overwrite(self.documentPath)

        try:
            os.remove(self.documentPath)
        except(FileNotFoundError):
            pass
        convert_file(self.mdPath, self._fileExtension, format='markdown_strict',
                     outputfile=self.documentPath)
        # Let pandoc convert markdown and write to .document file.
        os.remove(self.mdPath)
        if os.path.isfile(self.documentPath):
            self.postprocess()
            return(message.replace(self.mdPath, self.documentPath))

        else:
            return('ERROR: Could not create "' + self.documentPath + '".')

    def postprocess(self):
        pass

    def document_to_yw7(self):
        """Import from yw7 """

        if not os.path.isfile(self.documentPath):
            return('ERROR: "' + self.documentPath + '" not found.')

        convert_file(self.documentPath, 'markdown_strict', format=self._fileExtension,
                     outputfile=self.mdPath, extra_args=['--wrap=none'])
        # Let pandoc read the document file and convert to markdown.
        message = self.md_to_yw7()
        try:
            os.remove(self.mdPath)
        except(FileNotFoundError):
            pass
        return(message)
