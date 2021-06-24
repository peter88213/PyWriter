"""Provide a scene filter class for template-based file export.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScCrFilter():
    """Filter Scene per character.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, crId=None):
        self.character = crId

    def accept(self, source, id):
        """Return True if a source scene's character matches.
        """

        if self.character is not None:

            try:
                if self.character in source.scenes[id].characters:
                    return True

                else:
                    return False

            except:
                return False

        return True
