"""Build yWriter 7 project xml tree.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_tree_builder import YwTreeBuilder
import xml.etree.ElementTree as ET


class Yw7TreeBuilder(YwTreeBuilder):
    """Build yWriter 7 project xml tree."""

    def build_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        root = ywProject._tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if ywProject.scenes[scId].sceneContent is not None:
                scn.find(
                    'SceneContent').text = ywProject.scenes[scId].sceneContent
                scn.find('WordCount').text = str(
                    ywProject.scenes[scId].wordCount)
                scn.find('LetterCount').text = str(
                    ywProject.scenes[scId].letterCount)

            try:
                scn.remove(scn.find('RTFFile'))

            except:
                pass

        root.tag = 'YWRITER7'
        root.find('PROJECT').find('Ver').text = '7'
        ywProject._tree = ET.ElementTree(root)

        return YwTreeBuilder.build_element_tree(self, ywProject)
