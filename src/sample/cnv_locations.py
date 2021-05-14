"""Import and export yWriter location descriptions for editing. 

Convert yWriter location descriptions to odt with invisible location tags.
Convert html with invisible location tags to yWriter format.

This is a PyWriter sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_locations'

import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.universal_converter import UniversalConverter


def run(sourcePath, suffix=''):
    ui = UiTk('yWriter import/export')
    converter = UniversalConverter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
