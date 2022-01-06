"""Provide a scene per tag filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScTgFilter():
    """Filter Scene per tag.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, tag=None):
        self.tag = tag

    def accept(self, source, id):
        """Return True if a source scene's tag matches.
        """

        if self.tag is not None:

            try:
                if self.tag in source.scenes[id].tags:
                    return True

                else:
                    return False

            except:
                return False

        return True
