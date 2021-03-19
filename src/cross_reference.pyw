"""Generate cross references for a yWriterproject. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_xref'

import sys

from pywriter.converter.yw_cnv_tk import YwCnvTk
from pywriter.converter.export_file_factory import ExportFileFactory


class Converter(YwCnvTk):

    def __init__(self, silentMode=False):
        YwCnvTk.__init__(self, silentMode)
        self.fileFactory = ExportFileFactory()


if __name__ == '__main__':
    Converter().run(sys.argv[1], SUFFIX)
