"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.mdconverter import MdConverter
from pywriter.convert.pypandoc import convert_file


class OdtConverter(MdConverter):

    mdFile = 'temp.md'

    def yw7_to_odt(self, yw7File, odtFile):
        """ Export to odt """
        message = self.yw7_to_md(yw7File, self.mdFile)
        if message.count('ERROR'):
            return(message)

        if os.path.isfile(odtFile):
            self.confirm_overwrite(odtFile)

        try:
            os.remove(odtFile)
        except(FileNotFoundError):
            pass
        convert_file(self.mdFile, 'odt', format='markdown_strict',
                     outputfile=odtFile)
        # Let pandoc convert markdown and write to .odt file.
        os.remove(self.mdFile)
        if os.path.isfile(odtFile):
            return(message.replace(self.mdFile, odtFile))

        else:
            return('ERROR: Could not create "' + odtFile + '".')

    def odt_to_yw7(self, odtFile, yw7File):
        """ Import from yw7 """
        convert_file(odtFile, 'markdown_strict', format='odt',
                     outputfile=self.mdFile, extra_args=['--wrap=none'])
        # Let pandoc read .odt file and convert to markdown.
        message = self.md_to_yw7(self.mdFile, yw7File)
        try:
            os.remove(self.mdFile)
        except(FileNotFoundError):
            pass
        return(message)
