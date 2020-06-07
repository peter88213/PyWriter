"""Import a work in progress. 

Convert html with invisible chapter and scene tags to yWriter format.

Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.html.html_import import HtmlImport
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension == '.html':
        document = HtmlImport('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                         extension, silentMode, '')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
