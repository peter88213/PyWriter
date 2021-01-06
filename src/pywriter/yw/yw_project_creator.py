"""Fill a new yWriter project with the attributes of another.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_project_merger import YwProjectMerger


class YwProjectCreator(YwProjectMerger):
    """Create a new project.
    """

    def merge_projects(self, target, source):
        """Create target attributes with source attributes.
        Return a message beginning with SUCCESS or ERROR.
        """
        YwProjectMerger.merge_projects(self, target, source)
        return 'SUCCESS'
