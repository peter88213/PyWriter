"""Import and export ywriter7 scene list. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.converter.cnv_runner import CnvRunner
from pywriter.model.csvfile import CsvFile


def run(sourcePath, silentMode=True):
    document = CsvFile('')
    converter = CnvRunner(sourcePath, document, 'csv', silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
