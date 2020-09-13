"""Import an outline. 

Convert html with chapter and scene headings/descriptions to yWriter format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.html.html_outline import HtmlOutline
from pywriter.converter.yw_cnv_tk import YwCnvTk


def run(sourcePath, silentMode=True):
    converter = YwCnvTk(sourcePath, HtmlOutline.SUFFIX, silentMode)


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
