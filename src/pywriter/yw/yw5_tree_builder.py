"""Provide a strategy class to build an yWriter 5 xml tree.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.yw.yw7_tree_builder import Yw7TreeBuilder
import xml.etree.ElementTree as ET


class Yw5TreeBuilder(Yw7TreeBuilder):
    """Build yWriter 5 project xml tree."""

    TAG = 'YWRITER5'
    VER = '5'

    def convert_to_rtf(self, text):
        """Convert yw6/7 raw markup to rtf. 
        Return a rtf encoded string.
        """

        RTF_HEADER = '{\\rtf1\\ansi\\deff0\\nouicompat{\\fonttbl{\\f0\\fnil\\fcharset0 Courier New;}}{\\*\\generator PyWriter}\\viewkind4\\uc1 \\pard\\sa0\\sl240\\slmult1\\f0\\fs24\\lang9 '
        RTF_FOOTER = ' }'

        RTF_REPLACEMENTS = [
            ['\n\n', '\\line\\par '],
            ['\n', '\\par '],
            ['[i]', '{\\i '],
            ['[/i]', '}'],
            ['[b]', '{\\b '],
            ['[/b]', '}'],
            ['–', '--'],
            ['—', '--'],
            ['„', '\\u8222?'],
            ['‚', '\\u8218?'],
            ['‘', '\\lquote '],
            ['’', '\\rquote '],
            ['“', '\\ldblquote '],
            ['”', '\\rdblquote '],
            ['\u202f', '\\~'],
            ['»', '\\u0187?'],
            ['«', '\\u0171?'],
            ['›', '\\u8250?'],
            ['‹', '\\u8249?'],
            ['…', '\\u8230?'],
        ]

        try:

            for r in RTF_REPLACEMENTS:
                text = text.replace(r[0], r[1])

        except AttributeError:
            text = ''

        return RTF_HEADER + text + RTF_FOOTER

    def put_scene_contents(self, ywProject):
        """Modify the scene contents of an existing xml element tree.
        Write scene contents to RTF files.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """
        rtfDir = os.path.dirname(ywProject.filePath)

        if rtfDir == '':
            rtfDir = './RTF5'

        else:
            rtfDir += '/RTF5'

        for chId in ywProject.chapters:

            if ywProject.chapters[chId].oldType == 1:
                ywProject.chapters[chId].isUnused = False

        root = ywProject.tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            try:
                scn.remove(scn.find('SceneContent'))

            except:
                pass

            if ywProject.scenes[scId].rtfFile is not None:

                if scn.find('RTFFile') is None:
                    ET.SubElement(
                        scn, 'RTFFile').text = ywProject.scenes[scId].rtfFile

                if ywProject.scenes[scId].sceneContent is not None:
                    rtfPath = rtfDir + '/' + ywProject.scenes[scId].rtfFile

                    rtfScene = self.convert_to_rtf(
                        ywProject.scenes[scId].sceneContent)

                    try:

                        with open(rtfPath, 'w') as f:
                            f.write(rtfScene)

                    except:
                        return 'ERROR: Can not write scene file "' + rtfPath + '".'

        return 'SUCCESS'
