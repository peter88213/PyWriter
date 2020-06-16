"""Import and export yWriter character list. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.csv.csv_charlist import CsvCharList
from pywriter.converter.yw_cnv_gui import YwCnvGui
from pywriter.globals import CHARLIST_SUFFIX


def run(sourcePath, silentMode=True):
    document = CsvCharList('')
    converter = YwCnvGui(sourcePath, document, 'csv',
                         silentMode, CHARLIST_SUFFIX)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
