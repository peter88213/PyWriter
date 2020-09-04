"""yWNewFile - Class for yWriter xml file creation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator


class YwNewFile(YwFile):
    """yWriter xml project file representation."""

    def __init__(self, filePath):
        YwFile.__init__(self, filePath)
        self.ywTreeBuilder = Yw7TreeCreator()
