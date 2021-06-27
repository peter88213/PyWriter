"""Provide a scene per location filter class for template-based file export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScLcFilter():
    """Filter Scene per location.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, lcId=None):
        self.location = lcId

    def accept(self, source, id):
        """Return True if a source scene's location matches.
        """

        if self.location is not None:

            try:
                if self.location in source.scenes[id].locations:
                    return True

                else:
                    return False

            except:
                return False

        return True
