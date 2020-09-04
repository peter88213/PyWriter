"""Write yWriter 7 xml project file.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET
from pywriter.yw.yw_tree_writer import YwTreeWriter


class Yw7TreeWriter(YwTreeWriter):
    """Write yWriter 7 xml project file."""

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        root = ywProject._tree.getroot()
        root.tag = 'YWRITER7'
        root.find('PROJECT').find('Ver').text = '7'
        self.indent_xml(root)
        ywProject._tree = ET.ElementTree(root)

        try:
            ywProject._tree.write(
                ywProject._filePath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + ywProject._filePath + '" is write protected.'

        return 'SUCCESS'
