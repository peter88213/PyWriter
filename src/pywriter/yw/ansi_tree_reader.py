"""Provide a strategy class to read ANSI encoded yWriter projects.

DEPRECATED -- This module is no longer provided for v4.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET
from pywriter.yw.utf8_tree_reader import Utf8TreeReader


class AnsiTreeReader(Utf8TreeReader):
    """Read ANSI encoded yWriter xml project file."""

    def read_element_tree(self, ywProject):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        _TEMPFILE = '._tempfile.xml'

        try:

            with open(ywProject.filePath, 'r') as f:
                project = f.readlines()

            project[0] = project[0].replace('<?xml version="1.0" encoding="iso-8859-1"?>',
                                            '<?xml version="1.0" encoding="cp1252"?>')

            with open(_TEMPFILE, 'w') as f:
                f.writelines(project)

            ywProject.tree = ET.parse(_TEMPFILE)
            os.remove(_TEMPFILE)

        except:
            return 'ERROR: Can not process "' + os.path.normpath(ywProject.filePath) + '".'

        return 'SUCCESS: XML element tree read in.'
