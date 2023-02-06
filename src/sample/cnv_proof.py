"""Import and export yWriter scenes for editing. 

Convert yWriter to odt with visible chapter and scene tags.
Convert html with visible chapter and scene tags to yWriter format.

This is a PyWriter sample application.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_proof'

import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw7_converter import Yw7Converter


def run(sourcePath, suffix=''):
    ui = UiTk('yWriter import/export')
    converter = Yw7Converter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
