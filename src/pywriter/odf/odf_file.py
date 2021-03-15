"""OdfFile - Class for OpenDocument xml file generation.

Part of the PyWriter project.
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile

from pywriter.ods.ods_builder import OdsBuilder
from pywriter.file.file_export import FileExport


class OdfFile(FileExport, OdsBuilder):
    """OpenDocument xml project file representation.
    """

    EXTENSION = '.ods'
    # overwrites Novel.EXTENSION

    def convert_from_yw(self, text):
        """Convert yw7 raw markup to ods. Return an xml string.
        """

        ODS_REPLACEMENTS = [
            ['&', '&amp;'],  # must be first!
            ['"', '&quot;'],
            ["'", '&apos;'],
            ['>', '&gt;'],
            ['<', '&lt;'],
            ['\n', '</text:p>\n<text:p>'],
        ]

        try:
            text = text.rstrip()

            for r in ODS_REPLACEMENTS:
                text = text.replace(r[0], r[1])

        except AttributeError:
            text = ''

        return text

    def write(self):
        """Generate an ods file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Create a temporary directory containing the internal
        # structure of an ODS file except "content.xml".

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        # Add "content.xml" to the temporary directory.

        filePath = self._filePath

        self._filePath = self.TEMPDIR + '/content.xml'

        message = FileExport.write(self)

        self._filePath = filePath

        if message.startswith('ERROR'):
            return message

        # Pack the contents of the temporary directory
        # into the ODS file.

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odsTarget:
                os.chdir(self.TEMPDIR)

                for file in self.ODS_COMPONENTS:
                    odsTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + os.path.normpath(self.filePath) + '".'

        # Remove temporary data.

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + os.path.normpath(self.filePath) + '" written.'
