"""Import and export ywriter7 plot structure. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.csv.csv_plotlist import CsvPlotList
from pywriter.converter.cnv_runner import CnvRunner


def run(sourcePath, silentMode=True):
    document = CsvPlotList('')
    converter = CnvRunner(sourcePath, document, 'csv', silentMode, '_plot')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
