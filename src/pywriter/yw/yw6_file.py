"""yW6File - Class for yWriter 6 xml file operations and parsing.

Rewrite a yw7 project as yw5. Create rtf scene files.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET
from pywriter.yw.yw_file import YwFile


class Yw6File(YwFile):
    """yWriter 6 xml project file representation."""

    EXTENSION = '.yw6'
    # overwrites Novel._FILE_EXTENSION
    _VERSION = 6

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the correct extension. """

        if filePath.lower().endswith('.yw6'):
            self._filePath = filePath

    def write_element_tree(self, root):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        root.tag = 'YWRITER6'
        self._tree = ET.ElementTree(root)

        try:
            self._tree.write(
                self._filePath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        return 'SUCCESS'
