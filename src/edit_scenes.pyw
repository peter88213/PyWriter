"""Import and export yWriter scene descriptions for editing. 

Convert yWriter scene descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yWriter format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.converter.yw_cnv_tk import YwCnvTk


def run(sourcePath, silentMode=True):
    converter = YwCnvTk(sourcePath, OdtSceneDesc.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
