"""Import and export yWriter item descriptions for editing. 

Convert yWriter item descriptions to odt with invisible item tags.
Convert html with invisible item tags to yWriter format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.odt.odt_items import OdtItems
from pywriter.html.html_items import HtmlItems
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw5', '.yw6', '.yw7']:
        document = OdtItems('')
        extension = 'odt'

    elif FileExtension == '.html':
        document = HtmlItems('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                         extension, silentMode, HtmlItems.SUFFIX)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
