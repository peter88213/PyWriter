"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.mdconverter import MdConverter
from pywriter.pypandoc import convert_file


class OdtConverter(MdConverter):

    mdFile = 'temp.md'

    def __init__(self, yw7File, odtFile):
        MdConverter.__init__(self, yw7File, self.mdFile)
        self.odtFile = odtFile

    def yw7_to_odt(self):
        """ Export to odt """
        message = self.yw7_to_md()
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(self.odtFile):
            self.confirm_overwrite(self.odtFile)

        try:
            os.remove(self.odtFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, 'odt', format='markdown_strict',
                     outputfile=self.odtFile)
        # Let pandoc convert markdown and write to .odt file.
        os.remove(self.mdFile)
        if os.path.isfile(self.odtFile):
            return(message.replace(self.mdFile, self.odtFile))

        else:
            return('ERROR: Could not create "' + self.odtFile + '".')

    def odt_to_yw7(self):
        """ Import from yw7 """
        convert_file(self.odtFile, 'markdown_strict', format='odt',
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read .odt file and convert to markdown.
        message = self.md_to_yw7()
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)
