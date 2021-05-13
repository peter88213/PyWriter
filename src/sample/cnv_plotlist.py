"""Import and export yWriter plot structure. 

File format: csv (intended for spreadsheet conversion).

This is a PyWriter sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_plotlist'

import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.universal_converter import UniversalConverter


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = UniversalConverter()
    converter.ui = ui
    converter.run(sourcePath, suffix)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
