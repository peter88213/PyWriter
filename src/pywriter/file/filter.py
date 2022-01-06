"""Provide a generic filter class for template-based file export.

All specific filters inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Filter():
    """Strategy class, implementing filtering criteria 
    for template-based export.
    """

    def accept(self, source, id):
        """Return True if the entity is not to be filtered out.
        This is a stub to be overridden by subclass methods
        implementing filters.
        """
        return True
