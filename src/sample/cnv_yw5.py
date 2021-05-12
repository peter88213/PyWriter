"""Convert yWriter 7 to yWriter 5 format.

This is a PyWriter sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.ui.ui_cmd import UiCmd
from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.abstract_file_factory import AbstractFileFactory
from pywriter.converter.yw7_source_factory import Yw7SourceFactory
from pywriter.converter.yw5_target_factory import Yw5TargetFactory


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = YwCnvUi()
    converter.ui = ui
    converter.fileFactory = AbstractFileFactory()
    converter.fileFactory.exportSourceFactory = Yw7SourceFactory()
    converter.fileFactory.exportTargetFactory = Yw5TargetFactory()
    converter.run(sourcePath, suffix)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], None)
