"""Import and export yWriter scenes. 

Convert yWriter to odt format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.odt.odt_export import OdtExport
from pywriter.converter.yw_cnv_gui import YwCnvGui


def run(sourcePath, silentMode=True, stripChapterFromTitle=False):
    converter = YwCnvGui(sourcePath, OdtExport.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False, True)
