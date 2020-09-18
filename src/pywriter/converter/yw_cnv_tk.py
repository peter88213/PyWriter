"""Import and export yWriter data. 

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.ui import Ui
from pywriter.converter.ui_tk import UiTk
from pywriter.converter.file_factory import FileFactory


class YwCnvTk(YwCnvUi):
    """Standalone yWriter converter with a simple tkinter GUI. 
    """

    def __init__(self, sourcePath, suffix=None, silentMode=False):
        """Run the converter with a GUI. """

        if silentMode:
            self.userInterface = Ui('')

        else:
            self.userInterface = UiTk('yWriter import/export')

        self.fileFactory = FileFactory()

        # Run the converter.

        self.success = False
        self.run_conversion(sourcePath, suffix)
        self.userInterface.finish()
