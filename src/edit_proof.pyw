"""Import and export yWriter scenes for editing. 

Convert yWriter to odt with visible chapter and scene tags.
Convert html with visible chapter and scene tags to yWriter format.

Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os

from pywriter.odt.odt_proof import OdtProof
from pywriter.html.html_proof import HtmlProof
from pywriter.converter.yw_cnv_gui import YwCnvGui
from pywriter.globals import PROOF_SUFFIX


def run(sourcePath, silentMode=True):

    fileName, FileExtension = os.path.splitext(sourcePath)

    if FileExtension in ['.yw6', '.yw7']:
        document = OdtProof('')
        extension = 'odt'

    elif FileExtension == '.html':
        document = HtmlProof('')
        extension = 'html'

    else:
        sys.exit('ERROR: File type is not supported.')

    converter = YwCnvGui(sourcePath, document,
                         extension, silentMode, PROOF_SUFFIX)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
