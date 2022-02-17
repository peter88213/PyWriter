"""Provide a scene per item filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScItFilter():
    """Filter Scene per item.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, itId=None):
        self._item = itId

    def accept(self, source, eId):
        """Return True if a source scene's item matches.
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
