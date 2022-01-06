"""Provide a strategy class to read utf-8 encoded yWriter project files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET


class Utf8TreeReader():
    """Read utf-8 encoded yWriter xml project file."""

    def read_element_tree(self, ywProject):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        try:
            ywProject.tree = ET.parse(ywProject.filePath)

        except:
            return 'ERROR: Can not process "' + os.path.normpath(ywProject.filePath) + '".'

        return 'SUCCESS: XML element tree read in.'
