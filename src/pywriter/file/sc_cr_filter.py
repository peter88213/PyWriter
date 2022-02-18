"""Provide a scene per character filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScCrFilter():
    """Filter Scene per character.
    
    Public methods:
        accept -- check whether a scene is associated with the filter character.
    
    Strategy class, implementing filtering criteria for template-based scene export.
    """

    def __init__(self, crId=None):
        """Set the filter character."""
        self._character = crId

    def accept(self, source, eId):
        """Check whether a scene is associated with the filter character.
        
        Positional arguments:
            source -- Novel instance holding the scene to check.
            eId -- scene ID of the scene to check.       
        
        Return True if a source scene's character matches the filter character.
        Return True if no filter character is set. 
        Oherwise, return False.
        Overrides the superclass method.
        """

        if self._character is not None:

            try:
                if self._character in source.scenes[eId].characters:
                    return True

                else:
                    return False

            except:
                return False

        return True
