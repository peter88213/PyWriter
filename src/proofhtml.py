"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with visible chapter and scene tags

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
from pywriter.cmdline_ui.hcnv_runner import HCnvRunner


def run(sourcePath, silentMode=True):
    myConverter = HCnvRunner(sourcePath, 'html', silentMode)
    myConverter.run()


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
