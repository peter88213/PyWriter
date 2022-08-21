"""Provide a generic class for yWriter story world element representation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class BasicElement:
    """Basic element representation (may be a project note).
    
    Public instance variables:
        title -- str: title (name).
        desc -- str: description.
    """

    def __init__(self):
        """Initialize instance variables."""
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>
