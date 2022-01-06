"""Provide a scene per viewpoint filter class for template-based file export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class ScVpFilter():
    """Filter Scene per viewpoint.
    Strategy class, implementing filtering criteria 
    for template-based scene export.
    """

    def __init__(self, crId=None):
        self.viewpoint = crId

    def accept(self, source, id):
        """Return True if the source scene's viewpoint matches.
        """

        if self.viewpoint is not None:

            try:
                if self.viewpoint == source.scenes[id].characters[0]:
                    return True

                else:
                    return False

            except:
                return False

        return True
