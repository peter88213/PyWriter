"""PyWriter v1.3 - Import and export ywriter7 scenes for proofing. 

Proof reading file format: ODT (OASIS Open Document format) with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odtfile import OdtFile
from pywriter.model.htmlfile import HtmlFile
from pywriter.converter.hybrid_cnv import HybridCnv


def run(sourcePath, silentMode=True):
    sourceDoc = HtmlFile('')
    targetDoc = OdtFile('')
    targetDoc.proofread = True
    converter = HybridCnv(sourcePath, targetDoc, sourceDoc,
                          silentMode, '_proof')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
