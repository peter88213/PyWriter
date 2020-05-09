"""Object - represents the basic structure of an object in yWriter.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Object():
    """yWriter character representation."""

    def __init__(self):
        self.title = None
        # str

        self.desc = None
        # str

        self.tags = None
        # list of str

        self.aka = None
        # str
