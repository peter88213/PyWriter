"""yW5File - Class for yWriter 5 xml file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw5_tree_builder import Yw5TreeBuilder
from pywriter.yw.ansi_tree_reader import AnsiTreeReader
from pywriter.yw.ansi_tree_writer import AnsiTreeWriter
from pywriter.yw.ansi_postprocessor import AnsiPostprocessor


class Yw5File(YwFile):
    """yWriter 5 xml project file representation."""

    EXTENSION = '.yw5'

    def __init__(self, filePath):
        YwFile.__init__(self, filePath)
        self.ywTreeReader = AnsiTreeReader()
        self.ywTreeBuilder = Yw5TreeBuilder()
        self.ywTreeWriter = AnsiTreeWriter()
        self.ywPostprocessor = AnsiPostprocessor()
