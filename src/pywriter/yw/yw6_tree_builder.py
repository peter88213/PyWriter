"""Provide a strategy class to build an yWriter 6 xml tree.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw7_tree_builder import Yw7TreeBuilder


class Yw6TreeBuilder(Yw7TreeBuilder):
    """Build yWriter 6 project xml tree."""

    TAG = 'YWRITER6'
    VER = '5'

    def put_scene_contents(self, ywProject):
        """Modify the scene contents of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        root = ywProject.tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if ywProject.scenes[scId].sceneContent is not None:
                scn.find(
                    'SceneContent').text = ywProject.scenes[scId].sceneContent
                scn.find('WordCount').text = str(
                    ywProject.scenes[scId].wordCount)
                scn.find('LetterCount').text = str(
                    ywProject.scenes[scId].letterCount)

        return 'SUCCESS'
