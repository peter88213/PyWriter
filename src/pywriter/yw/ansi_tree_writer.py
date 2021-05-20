"""Provide a strategy class to write ANSI encoded yWriter project files.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from pywriter.yw.yw_tree_writer import YwTreeWriter


class AnsiTreeWriter(YwTreeWriter):
    """Write ANSI encoded yWriter project file."""

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        try:
            ywProject._tree.write(
                ywProject.filePath, xml_declaration=False, encoding='iso-8859-1')

        except(PermissionError):
            return 'ERROR: "' + os.path.normpath(ywProject.filePath) + '" is write protected.'

        return 'SUCCESS'
