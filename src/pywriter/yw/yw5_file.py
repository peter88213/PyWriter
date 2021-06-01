"""Provide a class for yWriter 5 project import and export.

Scene content can not be read in.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw5_tree_builder import Yw5TreeBuilder
from pywriter.yw.ansi_tree_reader import AnsiTreeReader
from pywriter.yw.yw_project_merger import YwProjectMerger
from pywriter.yw.ansi_tree_writer import AnsiTreeWriter
from pywriter.yw.ansi_postprocessor import AnsiPostprocessor


class Yw5File(Yw7File):
    """yWriter 5 project file representation."""

    DESCRIPTION = 'yWriter 5 project'
    EXTENSION = '.yw5'

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor.
        Initialize instance variables.
        """
        Yw7File.__init__(self, filePath)

        self.ywTreeReader = AnsiTreeReader()
        self.ywProjectMerger = YwProjectMerger()
        self.ywTreeBuilder = Yw5TreeBuilder()
        self.ywTreeWriter = AnsiTreeWriter()
        self.ywPostprocessor = AnsiPostprocessor()
