"""Provide a scene per item filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScItFilter():
    """Filter Scene per item.
    
    Public methods:
        accept(source, eId) -- check whether a scene is associated with the filter item.
    
    Strategy class, implementing filtering criteria for template-based scene export.
    """

    def __init__(self, itId=None):
        """Set the filter item."""
        self._item = itId

    def accept(self, source, eId):
        """Check whether a scene is associated with the filter item.
        
        Positional arguments:
            source -- Novel instance holding the scene to check.
            eId -- scene ID of the scene to check.       
        
        Return True if a source scene's item matches the filter item.
        Return True if no filter item is set. 
        Oherwise, return False.
        Overrides the superclass method.
        """

        if self._item is not None:

            try:
                if self._item in source.scenes[eId].items:
                    return True

                else:
                    return False

            except:
                return False

        return True
