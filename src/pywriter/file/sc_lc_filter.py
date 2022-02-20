"""Provide a scene per location filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScLcFilter():
    """Filter Scene per location.
    
    Public methods:
        accept(source, eId) -- check whether a scene is associated with the filter location.
    
    Strategy class, implementing filtering criteria for template-based scene export.
    """

    def __init__(self, lcId=None):
        """Set the filter location.
        
        Positional arguments:
            lcId -- str: filter location ID.
        """
        self._location = lcId

    def accept(self, source, eId):
        """Check whether a scene is associated with the filter location.
        
        Positional arguments:
            source -- Novel instance holding the scene to check.
            eId -- scene ID of the scene to check.       
        
        Return True if a source scene's location matches the filter location.
        Return True if no filter location is set. 
        Oherwise, return False.
        Overrides the superclass method.
        """

        if self._location is not None:

            try:
                if self._location in source.scenes[eId].locations:
                    return True

                else:
                    return False

            except:
                return False

        return True
