"""Import and export yWriter brief synopsis. 

This is a PyWriter sample application.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_brf_synopsis'

import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw7_exporter import Yw7Exporter


def run(sourcePath, suffix=''):
    ui = UiTk('yWriter import/export')
    converter = Yw7Exporter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
