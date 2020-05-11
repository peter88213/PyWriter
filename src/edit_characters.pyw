"""Import and export yWriter character descriptions for editing. 

Convert yWriter character descriptions to odt with invisible character tags.
Convert html with invisible character tags to yWriter format.

Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.odt.odt_characters import OdtCharacters
from pywriter.html.html_characters import HtmlCharacters
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw5', '.yw6', '.yw7']:
        document = OdtCharacters('')
        extension = 'odt'

    elif FileExtension == '.html':
        document = HtmlCharacters('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                         extension, silentMode, '_characters')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
