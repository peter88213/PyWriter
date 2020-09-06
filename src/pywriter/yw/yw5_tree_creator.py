"""Create a new yWriter 5 project xml tree 
from an existing yw7 project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from shutil import rmtree
import xml.etree.ElementTree as ET

from pywriter.yw.yw5_tree_builder import Yw5TreeBuilder


class Yw5TreeCreator(Yw5TreeBuilder):
    """Create a new yWriter 7 project xml tree."""

    def build_element_tree(self, ywProject):
        """Put the yWriter project attributes to a new xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy yw7 file.

        yw7File = os.path.splitext(self.filePath)[0] + '.yw7'

        try:
            with open(yw7File, 'rb') as f:
                project = f.read()

            with open(self.filePath, 'wb') as f:
                f.write(project)

        except:
            return 'ERROR: Can not copy "' + yw7File + ' to ' + self.filePath + '".'

        # Create RTF5 directory.

        rtfDir = os.path.split(ywProject.filePath)[0] + 'RTF5'

        try:
            rmtree(rtfDir)

        except:
            pass

        try:
            os.mkdir(rtfDir)

        except:
            return 'ERROR: cannot create scene dir "' + rtfDir + '".'

        # Create RTF file entries.

        sceneCount = 0

        for scId in ywProject.scenes:
            sceneCount += 1
            ywProject.scenes[scId].rtfFile = 'RTF_' + \
                str(sceneCount).zfill(5) + '.rtf'

        # Modify xml tree.

        try:
            ywProject._tree = ET.parse(ywProject._filePath)

        except:
            return 'ERROR: Can not read xml file "' + self._filePath + '".'

        message = Yw5TreeBuilder.build_element_tree(ywProject)
        return message
