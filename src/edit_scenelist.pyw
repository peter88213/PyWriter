"""Import and export yWriter scene list. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.csv.csv_scenelist import CsvSceneList
from pywriter.converter.yw_cnv_tk import YwCnvTk


def run(sourcePath, silentMode=True):
    converter = YwCnvTk(sourcePath, CsvSceneList.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
