"""Convert yWriter 7 to yWriter 5 format.

This is a PyWriter sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw_cnv_ui import YwCnvUi

from pywriter.yw.yw5_new_file import Yw5NewFile
from pywriter.yw.yw7_file import Yw7File


class MyConverter(YwCnvUi):
    EXPORT_SOURCE_CLASSES = [Yw7File]
    EXPORT_TARGET_CLASSES = [Yw5NewFile]


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = MyConverter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], None)
