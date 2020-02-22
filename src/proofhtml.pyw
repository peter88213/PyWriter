"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.html_proof import HtmlProof
from pywriter.converter.cnv_runner import CnvRunner


def run(sourcePath, silentMode=True):
    document = HtmlProof('')
    converter = CnvRunner(sourcePath, document, 'html', silentMode, '_proof')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
