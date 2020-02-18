"""PyWriter v1.3 - Import and export ywriter7 scene descriptions for editing. 

Convert yw7 scene descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yw7.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odt_scenedesc import OdtSceneDesc
from pywriter.model.html_scenedesc import HtmlSceneDesc
from pywriter.converter.hybrid_cnv import HybridCnv


def run(sourcePath, silentMode=True):
    sourceDoc = HtmlSceneDesc('')
    targetDoc = OdtSceneDesc('')
    converter = HybridCnv(sourcePath, targetDoc, sourceDoc,
                          silentMode, '_scenes')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
