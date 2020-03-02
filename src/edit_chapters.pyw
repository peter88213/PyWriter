"""PyWriter v1.4 - Import and export ywriter7 chapter descriptions for editing. 

Convert yw7 scene descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yw7.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.odt_chapterdesc_writer import OdtChapterDescWriter
from pywriter.model.html_chapterdesc_reader import HtmlChapterDescReader
from pywriter.converter.hybrid_cnv import HybridCnv


def run(sourcePath, silentMode=True):
    sourceDoc = HtmlChapterDescReader('')
    targetDoc = OdtChapterDescWriter('')
    converter = HybridCnv(sourcePath, targetDoc, sourceDoc,
                          silentMode, '_chapters')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
