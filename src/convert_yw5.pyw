"""Convert yw5. 

Convert yWriter 7 to yWriter 5 format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.yw.yw5_file import Yw5File
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True, stripChapterFromTitle=False):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw7']:
        document = Yw5File('')

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False, True)
