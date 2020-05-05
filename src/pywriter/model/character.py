"""Character - represents the basic structure of a character in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.object import Object


class Character(Object):
    """yWriter character representation."""

    def __init__(self):
        object.__init__(self)

        self.Notes = None
        # str

        self.bio = None
        # str

        self.goals = None
        # str

        self.fullName = None
        # str

        self.isMajor = None
        # bool