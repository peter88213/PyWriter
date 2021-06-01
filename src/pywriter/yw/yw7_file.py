"""Provide a class for yWriter 7 project import and export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw7_tree_builder import Yw7TreeBuilder
from pywriter.yw.utf8_tree_reader import Utf8TreeReader
from pywriter.yw.yw_project_merger import YwProjectMerger
from pywriter.yw.utf8_tree_writer import Utf8TreeWriter
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor


class Yw7File(YwFile):
    """yWriter 7 project file representation."""

    DESCRIPTION = 'yWriter 7 project'
    EXTENSION = '.yw7'

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor.
        Initialize instance variables.
        """
        YwFile.__init__(self, filePath)

        self.ywTreeReader = Utf8TreeReader()
        self.ywProjectMerger = YwProjectMerger()
        self.ywTreeBuilder = Yw7TreeBuilder()
        self.ywTreeWriter = Utf8TreeWriter()
        self.ywPostprocessor = Utf8Postprocessor()
