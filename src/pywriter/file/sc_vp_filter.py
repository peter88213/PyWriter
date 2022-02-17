"""Provide a scene per viewpoint filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScVpFilter():
    """Filter Scene per viewpoint.
    
    Public methods:
        accept -- check whether a scene's viewpoint matches the filter viewpoint.
    
    Strategy class, implementing filtering criteria for template-based scene export.
    """

    def __init__(self, crId=None):
        """Set the filter viewpoint."""
        self._viewpoint = crId

    def accept(self, source, eId):
        """Check whether a scene's viewpoint matches the filter viewpoint.
        
        Positional arguments:
            source -- Novel instance holding the scene to check.
            eId -- scene ID of the scene to check.
        
        Return True if the source scene's viewpoint matches the filter viewpoint.
        Return True if no filter viewpoint is set. 
        Oherwise, return False.
        Override the superclass method.
        """

        if self._viewpoint is not None:

            try:
                if self._viewpoint == source.scenes[eId].characters[0]:
                    return True

                else:
                    return False

            except:
                return False

        return True
