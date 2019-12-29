"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.mdconverter import MdConverter
from pywriter.pypandoc import convert_file


class DocxConverter(MdConverter):

    mdFile = 'temp.md'

    def __init__(self, yw7File, docxFile):
        MdConverter.__init__(self, yw7File, self.mdFile)
        self.docxFile = docxFile

    def yw7_to_docx(self):
        """ Export to docx """
        message = self.yw7_to_md()
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(self.docxFile):
            self.confirm_overwrite(self.docxFile)

        try:
            os.remove(self.docxFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, 'docx', format='markdown_strict',
                     outputfile=self.docxFile)
        # Let pandoc convert markdown and write to .docx file.
        os.remove(self.mdFile)
        if os.path.isfile(self.docxFile):
            return(message.replace(self.mdFile, self.docxFile))

        else:
            return('ERROR: Could not create "' + self.docxFile + '".')

    def docx_to_yw7(self):
        """ Import from yw7 """
        convert_file(self.docxFile, 'markdown_strict', format='docx',
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read .docx file and convert to markdown.
        message = self.md_to_yw7()
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)
