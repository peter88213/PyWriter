"""Convert yWriter to html format.



Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = ''

import sys
import os

from pywriter.ui.ui_cmd import UiCmd
from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.file_factory import FileFactory
from pywriter.yw.yw6_file import Yw6File
from pywriter.yw.yw7_file import Yw7File
from pywriter.html.html_export import HtmlExport


class HtmlFileFactory(FileFactory):
    """A factory class that instantiates a source file object
    and a target file object for conversion.
    """

    def get_file_objects(self, sourcePath, suffix=''):
        """Return a tuple with three elements:
        * A message string starting with 'SUCCESS' or 'ERROR'
        * sourceFile: a Novel subclass instance
        * targetFile: a Novel subclass instance
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        if fileExtension == Yw7File.EXTENSION:
            sourceFile = Yw7File(sourcePath)

        elif fileExtension == Yw6File.EXTENSION:
            sourceFile = Yw6File(sourcePath)

        else:
            return 'ERROR: File type is not supported.', None, None

        targetFile = HtmlExport(fileName + suffix + HtmlExport.EXTENSION)
        targetFile.SUFFIX = suffix

        return 'SUCCESS', sourceFile, targetFile


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = YwCnvUi(ui)
    converter.fileFactory = HtmlFileFactory()
    converter.run(sourcePath, suffix)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)
