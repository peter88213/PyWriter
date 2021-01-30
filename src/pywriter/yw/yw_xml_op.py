"""Interface for yWriter xml operations.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET
from pywriter.yw.yw_form import *


class XmlTreeReader():
    """Read yWriter xml project file."""

    def read_element_tree(self, ywFile):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        try:
            ywFile._tree = ET.parse(ywFile.filePath)

        except:
            return 'ERROR: Can not process "' + ywFile.filePath + '".'

        return 'SUCCESS: XML element tree read in.'


class XmlTreeWriter():
    """Write yWriter xml project file."""

    def write_element_tree(self, ywProject, root):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        root.tag = 'YWRITER7'
        root.find('PROJECT').find('Ver').text = '7'
        ywProject._tree = ET.ElementTree(root)

        try:
            ywProject._tree.write(
                ywProject.filePath, xml_declaration=False, encoding='utf-8')

        except(PermissionError):
            return 'ERROR: "' + ywProject.filePath + '" is write protected.'

        return 'SUCCESS'


class XmlPostprocessor():
    """Postprocess yWriter xml project file."""

    def postprocess_xml_file(self, ywFile):
        '''Postprocess the xml file created by ElementTree:
        Put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text.
        Return a message beginning with SUCCESS or ERROR.
        '''

        with open(ywFile.filePath, 'r', encoding='utf-8') as f:
            text = f.read()

        text = format_xml(text)
        text = '<?xml version="1.0" encoding="utf-8"?>\n' + text

        try:

            with open(ywFile.filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Can not write "' + ywFile.filePath + '".'

        return 'SUCCESS'
