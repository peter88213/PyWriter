"""Import and export XML data files. 

This is a PyWriter sample application.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_data'

import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw7_exporter import Yw7Exporter
from pywriter.yw.data_files import DataFiles


def run(sourcePath, suffix=''):
    DataFiles.SUFFIX = '_data'
    ui = UiTk('yWriter import/export')
    converter = Yw7Exporter()
    converter.ui = ui
    converter.EXPORT_TARGET_CLASSES.append(DataFiles)
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
