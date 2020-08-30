"""yWFile - Class for yWriter xml file operations and parsing.

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

        if text is None:
            text = ''

        text = text.replace('\n\n', '\\line\\par ').replace(
            '\n', '\\par ') + RTF_FOOTER
        text = text.replace('[i]', '{\\i ')
        text = text.replace('[/i]', '}')
        text = text.replace('[b]', '{\\b ')
        text = text.replace('[/b]', '}')
        return RTF_HEADER + text

    def write(self):
        """Copy and modify a yWriter 7 xml file to 
        generate a yWriter 5 project.  
        Return a message beginning with SUCCESS or ERROR.
        """

        # Read yw7 file.

        yw7File = os.path.splitext(self.filePath)[0] + '.yw7'

        try:
            with open(yw7File, 'r', encoding='utf-8-sig') as f:
                xmlText = f.read()
        except:
            return 'ERROR: Can not read"' + yw7File + '".'

        # Modify xml header and root structure.

        xmlText = xmlText.replace('encoding="utf-8"', 'encoding="' + self._ENCODING + '"').replace(
            'YWRITER7>', 'YWRITER5>').replace('<Ver>7</Ver>', '<Ver>5</Ver>')

        #  Write yw5 file.

        try:
            with open(self.filePath, 'w', encoding=self._ENCODING) as f:
                f.write(xmlText)
        except:
            return 'ERROR: Can not write project file "' + self.filePath + '".'

        # Create RTF5 directory.

        rtfDir = os.path.split(self.filePath)[0] + 'RTF5'

        try:
            rmtree(rtfDir)
        except:
            pass

        try:
            os.mkdir(rtfDir)
        except OSError:
            pass
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

            with open(rtfPath, 'w', encoding=self._ENCODING) as f:
                f.write(rtfScene)

        # Modify xml tree.

        try:
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()
        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        message = YwFile.write(self)
        return message
