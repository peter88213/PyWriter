"""Provide a strategy class to build a new yWriter 5 xml tree.

DEPRECATED -- This module is no longer provided for v4.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from shutil import rmtree
import xml.etree.ElementTree as ET

from pywriter.yw.yw5_tree_builder import Yw5TreeBuilder


class Yw5TreeCreator(Yw5TreeBuilder):
    """Create a yw5 project xml tree from an existing yw7 project."""

    def build_element_tree(self, ywProject):
        """Put the yWriter project attributes to a new xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy yw7 file.

        yw7File = os.path.splitext(ywProject.filePath)[0] + '.yw7'

        try:
            with open(yw7File, 'rb') as f:
                project = f.read()

            with open(ywProject.filePath, 'wb') as f:
                f.write(project)

        except:
            return 'ERROR: Can not copy "' + yw7File + ' to ' + ywProject.filePath + '".'

        # Create RTF5 directory.

        rtfDir = os.path.dirname(ywProject.filePath)

        if rtfDir == '':
            rtfDir = './RTF5'

        else:
            rtfDir += '/RTF5'

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
            ywProject.tree = ET.parse(ywProject.filePath)

        except:
            return 'ERROR: Can not read xml file "' + ywProject.filePath + '".'

        return Yw5TreeBuilder.build_element_tree(self, ywProject)
