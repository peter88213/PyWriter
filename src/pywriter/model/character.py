"""Provide a class for yWriter character representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.world_element import WorldElement


class Character(WorldElement):
    """yWriter character representation.

    Public instance variables:
        notes -- character notes in a single string.
        bio -- character biography in a single string.
        goals -- character's goals in the story in a single string.
        fullName -- full name (the title inherited may be a short name).
        isMajor -- True, if it's a major character.
    """

    MAJOR_MARKER = 'Major'
    MINOR_MARKER = 'Minor'

    def __init__(self):
        """Extend the superclass constructor by adding instance variables."""
        super().__init__()

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
