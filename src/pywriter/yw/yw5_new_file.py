"""Provide a class for yWriter 5 project creation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw5_file import Yw5File
from pywriter.yw.yw5_tree_creator import Yw5TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator


class Yw5NewFile(Yw5File):
    """yWriter 7 new project file representation."""

    def __init__(self, filePath, **kwargs):
        """Extends the super class constructor."""
        Yw5File.__init__(self, filePath)

        self.ywProjectMerger = YwProjectCreator()
        self.ywTreeBuilder = Yw5TreeCreator()
