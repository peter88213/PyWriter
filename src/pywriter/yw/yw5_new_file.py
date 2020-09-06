"""yW5File - Class for yWriter xml file operations and parsing.

Rewrite a yw7 project as yw5. Create rtf scene files.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw5_tree_creator import Yw5TreeCreator


class Yw5NewFile(YwFile):
    """yWriter 5 xml project file representation."""

    EXTENSION = '.yw5'

    def write(self):
        self.ywTreeBuilder = Yw5TreeCreator()
        return YwFile.write(self)
