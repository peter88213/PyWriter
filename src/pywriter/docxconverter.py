"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.mdconverter import MdConverter
from pywriter.convert.pypandoc import convert_file


class DocxConverter(MdConverter):

    mdFile = 'temp.md'

    def yw7_to_docx(self, yw7File, docxFile):
        """ Export to docx """
        message = self.yw7_to_md(yw7File, self.mdFile)
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(docxFile):
            self.confirm_overwrite(docxFile)

        try:
            os.remove(docxFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, 'docx', format='markdown_strict',
                     outputfile=docxFile)
        # Let pandoc convert markdown and write to .docx file.
        os.remove(self.mdFile)
        if os.path.isfile(docxFile):
            return(message.replace(self.mdFile, docxFile))

        else:
            return('ERROR: Could not create "' + docxFile + '".')

    def docx_to_yw7(self, docxFile, yw7File):
        """ Import from yw7 """
        convert_file(docxFile, 'markdown_strict', format='docx',
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read .docx file and convert to markdown.
        message = self.md_to_yw7(self.mdFile, yw7File)
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)
