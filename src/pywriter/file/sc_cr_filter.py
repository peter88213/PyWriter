"""Provide a scene per character filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScCrFilter():
    """Filter Scene per character.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, crId=None):
        self._character = crId

    def accept(self, source, eId):
        """Return True if a source scene's character matches.
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
