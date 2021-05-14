"""Provide a class for yWriter 7 xml file creation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator


class Yw7NewFile(Yw7File):
    """yWriter 7 new project file representation."""

    def __init__(self, filePath, **kwargs):
        """Extends the superclass constructor."""
        Yw7File.__init__(self, filePath)

        self.ywProjectMerger = YwProjectCreator()
        self.ywTreeBuilder = Yw7TreeCreator()
