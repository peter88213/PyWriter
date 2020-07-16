"""Import and export yWriter scenes. 

Convert yWriter to odt format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.odt.odt_export import OdtExport
from pywriter.converter.yw_cnv_gui import YwCnvGui
from pywriter.model.chapter import Chapter


def run(sourcePath, silentMode=True, stripChapterFromTitle=False):

    Chapter.stripChapterFromTitle = stripChapterFromTitle
    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw6', '.yw7']:
        document = OdtExport('')

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False, True)
