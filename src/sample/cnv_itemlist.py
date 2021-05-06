"""Import and export yWriter item list. 

File format: csv (intended for spreadsheet conversion).

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_itemlist'

import sys

from pywriter.ui.ui_cmd import UiCmd
from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.universal_file_factory import UniversalFileFactory


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = YwCnvUi(ui)
    converter.fileFactory = UniversalFileFactory()
    converter.run(sourcePath, suffix)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
