"""Read yWriter project.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from abc import abstractmethod


class YwTreeReader():
    """Read yWriter xml project file."""

    @abstractmethod
    def read_element_tree(self, ywFile):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """
