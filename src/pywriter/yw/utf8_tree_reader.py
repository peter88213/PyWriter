"""Read utf-8 encoded yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET
from pywriter.yw.yw_tree_reader import YwTreeReader


class Utf8TreeReader(YwTreeReader):
    """Read yWriter xml project file."""

    def read_element_tree(self, ywFile):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        try:
            ywFile._tree = ET.parse(ywFile.filePath)

        except:
            return 'ERROR: Can not process "' + os.path.normpath(ywFile.filePath) + '".'

        return 'SUCCESS: XML element tree read in.'
