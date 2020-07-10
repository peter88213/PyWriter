"""Character - represents the basic structure of a character in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.object import Object


class Character(Object):
    """yWriter character representation.
    # xml: <CHARACTERS><CHARACTER>
    """

    def __init__(self):
        Object.__init__(self)

        self.notes = None
        # str
        # xml: <Notes>

        self.bio = None
        # str
        # xml: <Bio>

        self.goals = None
        # str
        # xml: <Goals>

        self.fullName = None
        # str
        # xml: <FullName>

        self.isMajor = None
        # bool
        # xml: <Major>

    def merge(self, character):
        """Merge attributes.
        """
        Object.merge(self, character)

        if character.notes is not None:
            self.notes = character.notes

        if character.bio is not None:
            self.bio = character.bio

        if character.goals is not None:
            self.goals = character.goals

        if character.fullName is not None:
            self.fullName = character.fullName

        if character.isMajor is not None:
            self.isMajor = character.isMajor
