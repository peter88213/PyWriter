"""PyWriter v1.2 - Import and export ywriter7 scenes for editing. 

Proof reading file format: html (with invisible chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import subprocess

from pywriter.model.odtfile import OdtFile
from pywriter.model.yw7file import Yw7File


TITLE = 'yW2OO v2.1'

LIBREOFFICE = ['c:/Program Files/LibreOffice/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice/program/swriter.exe',
               'c:/Program Files/LibreOffice 5/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice 5/program/swriter.exe']


SUFFIX = '_exp'
# File name suffix for the exported html file.
# Example:
# foo.yw7 --> foo_exp.html


def main():
    sourcePath = None

    templatePath = os.environ['USERPROFILE'] + \
        '/AppData/Roaming/LibreOffice/4/user/yW2OO/template.zip'

    if not os.path.isfile(templatePath):
        return 'ERROR: "' + templatePath + '" not found.'

    files = os.listdir('.')

    for file in files:

        if '.yw7' in file:
            sourcePath = file
            break

    if sourcePath is None:
        return 'ERROR: No yWriter 7 project found.'

    print('Export yWriter7 scenes content to odt')
    print('Project: "' + sourcePath + '"')
    yw7File = Yw7File(sourcePath)

    if yw7File.is_locked():
        return 'ERROR: yWriter 7 seems to be open. Please close first.'

    message = yw7File.read()

    if message.startswith('ERROR'):
        return (message)

    document = OdtFile(sourcePath.split('.yw7')[
                       0] + SUFFIX + '.odt', templatePath)
    document.comments = True
    message = document.write(yw7File)

    if message.startswith('ERROR'):
        return (message)

    if startWriter:

        for lo in LIBREOFFICE:

            if os.path.isfile(lo):
                cmd = [os.path.normpath(lo)]
                cmd.append('macro:///yW2OO.Convert.main')
                cmd.append(document.filePath)
                subprocess.call(cmd)

    return (message)


if __name__ == '__main__':
    startWriter = False
    print(main())
