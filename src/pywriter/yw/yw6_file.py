"""Provide a class for yWriter 6 project import and export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw6_tree_builder import Yw6TreeBuilder
from pywriter.yw.utf8_tree_reader import Utf8TreeReader
from pywriter.yw.yw_project_merger import YwProjectMerger
from pywriter.yw.utf8_tree_writer import Utf8TreeWriter
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor


class Yw6File(YwFile):
    """yWriter 6 project file representation."""

    DESCRIPTION = 'yWriter 6 project'
    EXTENSION = '.yw6'

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor.
        Initialize instance variables.
        """
        YwFile.__init__(self, filePath)

        self.ywTreeReader = Utf8TreeReader()
        self.ywProjectMerger = YwProjectMerger()
        self.ywTreeBuilder = Yw6TreeBuilder()
        self.ywTreeWriter = Utf8TreeWriter()
        self.ywPostprocessor = Utf8Postprocessor()
