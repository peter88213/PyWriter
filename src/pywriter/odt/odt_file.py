"""OdtFile - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import zipfile

from pywriter.odt.odt_template import OdtTemplate
from pywriter.file.file_export import FileExport
from pywriter.odt.odt_form import *


class OdtFile(FileExport, OdtTemplate):
    """OpenDocument xml project file representation."""
    _FILE_EXTENSION = '.odt'

    fileHeader = ''
    partTemplate = ''
    chapterTemplate = ''
    sceneTemplate = ''
    sceneDivider = ''
    characterTemplate = ''
    locationTemplate = ''
    itemTemplate = ''
    fileFooter = ''

    def convert_markup(self, text):
        """Convert yw7 raw markup to odt. Return an xml string."""

        try:

            # process italics and bold markup reaching across linebreaks

            italics = False
            bold = False
            newlines = []
            lines = text.split('\n')
            for line in lines:
                if italics:
                    line = '[i]' + line
                    italics = False

                while line.count('[i]') > line.count('[/i]'):
                    line += '[/i]'
                    italics = True

                while line.count('[/i]') > line.count('[i]'):
                    line = '[i]' + line

                line = line.replace('[i][/i]', '')

                if bold:
                    line = '[b]' + line
                    bold = False

                while line.count('[b]') > line.count('[/b]'):
                    line += '[/b]'
                    bold = True

                while line.count('[/b]') > line.count('[b]'):
                    line = '[b]' + line

                line = line.replace('[b][/b]', '')

                newlines.append(line)

            text = '\n'.join(newlines)
            text = text.replace('&', '&amp;')
            text = text.replace('>', '&gt;')
            text = text.replace('<', '&lt;')
            text = text.rstrip().replace(
                '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
            text = text.replace(
                '[i]', '<text:span text:style-name="Emphasis">')
            text = text.replace('[/i]', '</text:span>')
            text = text.replace(
                '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
            text = text.replace('[/b]', '</text:span>')

        except AttributeError:
            text = ''

        return text

    def write(self):
        """Generate an odt file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Create a temporary directory containing the internal
        # structure of an ODT file except "content.xml".

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        # Add "content.xml" to the temporary directory.

        filePath = self._filePath

        self._filePath = self._TEMPDIR + '/content.xml'

        message = FileExport.write(self)

        self._filePath = filePath

        if message.startswith('ERROR'):
            return message

        # Pack the contents of the temporary directory
        # into the ODT file.

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                os.chdir(self._TEMPDIR)

                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        # Remove temporary data.

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'
