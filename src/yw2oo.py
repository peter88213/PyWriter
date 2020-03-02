"""PyWriter v1.3 - Export ywriter7 scenes. 

File format: odt (without chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.model.odtfile_writer import OdtFileWriter
from pywriter.model.yw7file import Yw7File


TITLE = 'yW2OO v2.2'

LIBREOFFICE = ['c:/Program Files/LibreOffice/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice/program/swriter.exe',
               'c:/Program Files/LibreOffice 5/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice 5/program/swriter.exe']


SUFFIX = ''
# File name suffix for the exported odt file.
# Example:
# foo.yw7 --> foo_exp.odt


def main():
    sourcePath = None

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
        return message

    document = OdtFileWriter(sourcePath.split('.yw7')[0] + SUFFIX + '.odt')
    document.comments = True
    message = document.write(yw7File)
    return message


if __name__ == '__main__':
    message = main()
    print(message)
