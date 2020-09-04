"""Postprocess ANSI encoded yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_postprocessor import YwPostprocessor


class AnsiPostprocessor(YwPostprocessor):
    """Postprocess ANSI encoded yWriter project."""

    def postprocess_xml_file(self, ywFile):
        '''Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        with open(ywFile.filePath, 'r') as f:
            text = f.read()

        text = self.format_xml(text)
        text = '<?xml version="1.0" encoding="iso-8859-1"?>\n' + text

        try:

            with open(ywFile.filePath, 'w') as f:
                f.write(text)

        except:
            return 'ERROR: Can not write "' + ywFile.filePath + '".'

        return 'SUCCESS'
