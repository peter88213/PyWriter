"""Provide a strategy class to postprocess ANSI encoded yWriter project files.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor


class AnsiPostprocessor(Utf8Postprocessor):
    """Postprocess ANSI encoded yWriter project."""

    def postprocess_xml_file(self, filePath):
        '''Override the superclass method.
        Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        with open(filePath, 'r') as f:
            text = f.read()

        text = self.format_xml(text)
        text = '<?xml version="1.0" encoding="iso-8859-1"?>\n' + text

        try:

            with open(filePath, 'w') as f:
                f.write(text)

        except:
            return 'ERROR: Can not write "' + os.path.normpath(filePath) + '".'

        return 'SUCCESS: "' + os.path.normpath(filePath) + '" written.'
