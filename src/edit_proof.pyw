"""Import and export yWriter scenes for editing. 

Convert yWriter to odt with visible chapter and scene tags.
Convert html with visible chapter and scene tags to yWriter format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.odt.odt_proof import OdtProof
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True):
    converter = YwCnvGui(sourcePath, OdtProof.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
