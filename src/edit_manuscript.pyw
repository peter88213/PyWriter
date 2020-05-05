"""Import and export yWriter scenes for editing. 

Convert yWriter to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yWriter format.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw5', '.yw6', '.yw7']:
        document = OdtManuscript('')
        extension = 'odt'

    elif FileExtension == '.html':
        document = HtmlManuscript('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                         extension, silentMode, '_manuscript')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
