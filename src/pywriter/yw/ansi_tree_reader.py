"""Read ANSI encoded yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import xml.etree.ElementTree as ET
from pywriter.yw.yw_tree_reader import YwTreeReader


class AnsiTreeReader(YwTreeReader):
    """Read yWriter xml project file."""

    def read_element_tree(self, ywFile):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        _TEMPFILE = '._tempfile.xml'

        try:

            with open(ywFile.filePath, 'r') as f:
                project = f.readlines()

            project[0] = project[0].replace('<?xml version="1.0" encoding="iso-8859-1"?>',
                                            '<?xml version="1.0" encoding="cp1252"?>')

            with open(_TEMPFILE, 'w') as f:
                f.writelines(project)

            ywFile._tree = ET.parse(_TEMPFILE)
            os.remove(_TEMPFILE)

        except:
            return 'ERROR: Can not process "' + os.path.normpath(ywFile._filePath) + '".'

        return 'SUCCESS: XML element tree read in.'
