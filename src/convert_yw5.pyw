"""Convert yw5. 

Convert yWriter 7 to yWriter 5 format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.yw.yw5_file import Yw5File
from pywriter.converter.yw_cnv_tk import YwCnvTk


def run(sourcePath, silentMode=True):
    converter = YwCnvTk(sourcePath, Yw5File.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
