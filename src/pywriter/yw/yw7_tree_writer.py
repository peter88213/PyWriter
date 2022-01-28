"""Provide a strategy class to write utf-8 encoded yWriter project files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os


class Yw7TreeWriter():
    """Write utf-8 encoded yWriter project file.

    Public methods: 
        write_element_tree(ywProject) -- Write back the xml element tree to a yw7 file.   
    """

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        """

        if os.path.isfile(ywProject.filePath):
            os.replace(ywProject.filePath, ywProject.filePath + '.bak')
            backedUp = True

        else:
            backedUp = False

        try:
            ywProject.tree.write(ywProject.filePath, xml_declaration=False, encoding='utf-8')

        except:

            if backedUp:
                os.replace(ywProject.filePath + '.bak', ywProject.filePath)

            return 'ERROR: Cannot write "{}".'.format(os.path.normpath(ywProject.filePath))

        return 'SUCCESS'
