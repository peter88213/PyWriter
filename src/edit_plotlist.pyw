"""Import and export yWriter plot structure. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.csv.csv_plotlist import CsvPlotList
from pywriter.converter.yw_cnv_tk import YwCnvTk


def run(sourcePath, silentMode=True):
    converter = YwCnvTk(sourcePath, CsvPlotList.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
