"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = ODT (OASIS Open Document format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
from pywriter.cmdline_ui.dcnv_runner import DCnvRunner


def run(sourcePath, silentMode=True):
    myConverter = DCnvRunner(sourcePath, 'odt', silentMode)
    myConverter.run()


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
