"""PyWriter v1.2 - Import and export ywriter7 scenes for editing. 

Proof reading file format: html (with invisible chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
from pywriter.gui.mcnv_runner import MCnvRunner

from pywriter.edit.manuscript import Manuscript


def run(sourcePath, silentMode=True):
    document = Manuscript('')
    converter = MCnvRunner(sourcePath, document, '_manuscript', silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
