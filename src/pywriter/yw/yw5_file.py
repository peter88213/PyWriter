"""yW5File - Class for yWriter xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from shutil import rmtree
import xml.etree.ElementTree as ET

from pywriter.yw.yw_file import YwFile


class Yw5File(YwFile):
    """yWriter 5 xml project file representation."""

    EXTENSION = '.yw5'
    # overwrites Novel._FILE_EXTENSION

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
        ]

        try:

            for r in RTF_REPLACEMENTS:
                text = text.replace(r[0], r[1])

        except AttributeError:
            text = ''

        return RTF_HEADER + text + RTF_FOOTER

    def write(self):
        """Copy and modify a yWriter 7 xml file to 
        generate a yWriter 5 project.  
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

        rtfDir = os.path.split(self.filePath)[0] + 'RTF5'

        try:
            rmtree(rtfDir)

        except:
            pass

        try:
            os.mkdir(rtfDir)

        except:
            return 'ERROR: cannot create scene dir "' + rtfDir + '".'

        # Create RTF files.

        sceneCount = 0

        for scId in self.scenes:
            sceneCount += 1
            self.scenes[scId].rtfFile = 'RTF_' + \
                str(sceneCount).zfill(5) + '.rtf'
            rtfPath = rtfDir + '/' + self.scenes[scId].rtfFile
            rtfScene = self.convert_to_rtf(self.scenes[scId].sceneContent)

            with open(rtfPath, 'w') as f:
                f.write(rtfScene)

        # Modify xml tree.

        try:
            self._tree = ET.parse(self._filePath)

        except:
            return 'ERROR: Can not read xml file "' + self._filePath + '".'

        message = YwFile.write(self)
        return message
