"""Import and export ywriter7 scene list. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.scenelist import SceneList
from pywriter.converter.cnv_runner import CnvRunner


def run(sourcePath, silentMode = True):
    document = SceneList('')
    converter = CnvRunner(sourcePath, document, 'csv', silentMode, '_scenes')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
