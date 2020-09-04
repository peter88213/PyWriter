"""Build yWriter 5 project xml tree.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_tree_builder import YwTreeBuilder
import xml.etree.ElementTree as ET


class Yw5TreeBuilder(YwTreeBuilder):
    """Build yWriter 5 project xml tree."""

    def build_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """
        for chId in ywProject.chapters:

            if ywProject.chapters[chId].oldType == 1:
                ywProject.chapters[chId].isUnused = False

        root = ywProject._tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            try:
                scn.remove(scn.find('SceneContent'))

            except:
                pass

            if ywProject.scenes[scId].sceneContent is not None:
                pass

            if scn.find('RTFFile') is None:
                ET.SubElement(scn, 'RTFFile')

            try:
                scn.find('RTFFile').text = ywProject.scenes[scId].rtfFile
            except:
                return 'ERROR: yWriter 5 RTF file not generated.'

        root.tag = 'YWRITER5'
        root.find('PROJECT').find('Ver').text = '5'
        ywProject._tree = ET.ElementTree(root)

        return YwTreeBuilder.build_element_tree(self, ywProject)
