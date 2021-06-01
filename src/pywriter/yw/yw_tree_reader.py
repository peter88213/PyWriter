"""Provide an abstract strategy class to read yWriter project files.

yWriter version-specific tree readers inherit from this class.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class YwTreeReader():
    """Read yWriter xml project file."""

    def read_element_tree(self, ywProject):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        To be overridden by file format specific subclasses.
        """
