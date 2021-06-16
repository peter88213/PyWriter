"""Provide a class for yWriter 5 project creation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw5_tree_creator import Yw5TreeCreator


class Yw5NewFile(Yw5File):
    """yWriter 5 new project file representation."""

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        Extend the superclass constructor by changing the
        ywProjectMerger and ywTreeBuilder strategies.
        """
        Yw5File.__init__(self, filePath)

        self.ywTreeBuilder = Yw5TreeCreator()
