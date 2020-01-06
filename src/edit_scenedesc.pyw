"""PyWriter v1.x - Import and export ywriter7 scenes for proofing. 

Proof reading file format: html (with invisible chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
from pywriter.gui.scnv_runner import SCnvRunner


def run(sourcePath, silentMode=True):
    myConverter = SCnvRunner(sourcePath, '_scenedesc', silentMode)
    myConverter.run()


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
