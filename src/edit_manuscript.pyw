"""PyWriter v1.3 - Import and export ywriter7 scenes for editing. 

Convert yw7 to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yw7.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odt_manuscript import OdtManuscript
from pywriter.model.html_manuscript import HtmlManuscript
from pywriter.converter.hybrid_cnv import HybridCnv


def run(sourcePath, silentMode=True):
    sourceDoc = HtmlManuscript('')
    targetDoc = OdtManuscript('')
    converter = HybridCnv(sourcePath, targetDoc, sourceDoc,
                          silentMode, '_manuscript')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
