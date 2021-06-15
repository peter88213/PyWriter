"""Provide a class for yWriter 7 project creation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw_project_creator import YwProjectCreator


class Yw7NewFile(Yw7File):
    """yWriter 7 new project file representation."""

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        Extend the superclass constructor by changing the
        ywProjectMerger and ywTreeBuilder strategies.
        """
        Yw7File.__init__(self, filePath)

        self.ywProjectMerger = YwProjectCreator()
