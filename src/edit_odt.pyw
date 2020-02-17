"""PyWriter v1.2 - Import and export ywriter7 scenes for editing. 

Proof reading file format: html (with invisible chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odtfile import OdtFile
from pywriter.model.manuscript import Manuscript
from pywriter.converter.hybrid_cnv import HybridCnv


def run(sourcePath, silentMode=True):
    sourceDoc = Manuscript('')
    targetDoc = OdtFile('')
    targetDoc.comments = True
    targetDoc.sections = True
    targetDoc.bookmarks = True
    converter = HybridCnv(sourcePath, targetDoc, sourceDoc,
                          silentMode, '_manuscript')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
