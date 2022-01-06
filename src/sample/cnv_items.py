"""Import and export yWriter item descriptions for editing. 

Convert yWriter item descriptions to odt with invisible item tags.
Convert html with invisible item tags to yWriter format.

This is a PyWriter sample application.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_items'

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
