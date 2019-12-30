"""Import and export ywriter7 scenes for proofing.

Proof reading Office document

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.proof.mdconverter import MdConverter
from pywriter.proof.pypandoc import convert_file


class DocumentConverter(MdConverter):

    mdFile = 'temp.md'
    _fileExtensions = ['docx', 'html', 'odt']

    def __init__(self, yw7File, documentFile):
        MdConverter.__init__(self, yw7File, self.mdFile)
        self.documentFile = documentFile
        nameParts = self.documentFile.split('.')
        self.fileExtension = nameParts[len(nameParts) - 1]

    @property
    def fileExtension(self):
        return(self._fileExtension)

    @fileExtension.setter
    def fileExtension(self, fileExt):
        if fileExt in self._fileExtensions:
            self._fileExtension = fileExt

    def yw7_to_document(self):
        """ Export to document """
        message = self.yw7_to_md()
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(self.documentFile):
            self.confirm_overwrite(self.documentFile)

        try:
            os.remove(self.documentFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, self.fileExtension, format='markdown_strict',
                     outputfile=self.documentFile)
        # Let pandoc convert markdown and write to .document file.
        os.remove(self.mdFile)
        if os.path.isfile(self.documentFile):
            return(message.replace(self.mdFile, self.documentFile))

        else:
            return('ERROR: Could not create "' + self.documentFile + '".')

    def document_to_yw7(self):
        """ Import from yw7 """
        convert_file(self.documentFile, 'markdown_strict', format=self._fileExtension,
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read the document file and convert to markdown.
        message = self.md_to_yw7()
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)
