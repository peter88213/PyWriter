"""Provide a strategy class to create a new yWriter project structure.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_project_merger import YwProjectMerger


class YwProjectCreator(YwProjectMerger):
    """Extend the super class by disabling its project structure check."""

    def merge_projects(self, target, source):
        """Copy source attributes to the target.
        Return a message beginning with SUCCESS, even if the source and 
        target project structures are inconsistent. Thus the source
        project can be merged with an empty target, creating a new project.
        """
        YwProjectMerger.merge_projects(self, target, source)
        return 'SUCCESS'
