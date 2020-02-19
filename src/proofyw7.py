"""PyWriter v1.3 - Import and export ywriter7 scenes for proofing. 

Proof reading file format: ODT (OASIS Open Document format) with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odt_proof import OdtProof
from pywriter.model.html_proof import HtmlProof
from pywriter.converter.lo_cnv import LoCnv


def run(sourcePath):
    sourcePath = sourcePath.replace('file:///', '').replace('%20', ' ')
    sourceDoc = HtmlProof('')
    targetDoc = OdtProof('')
    converter = LoCnv()
    message = converter.run(sourcePath, targetDoc, sourceDoc, '_proof')
    return message


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    print(run(sourcePath))
