"""Provide a class for yWriter 6 project import and export.

DEPRECATED -- This module is no longer provided for v4.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw6_tree_builder import Yw6TreeBuilder


class Yw6File(Yw7File):
    """yWriter 6 project file representation."""

    DESCRIPTION = 'yWriter 6 project'
    EXTENSION = '.yw6'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        Extend the superclass constructor by changing
        the ywTreeBuilder strategy. 
        """
        Yw7File.__init__(self, filePath)

        self.ywTreeBuilder = Yw6TreeBuilder()
