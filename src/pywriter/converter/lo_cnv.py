"""Import and export yWriter 7 data. 

Standalone yWriter 7 converter to be called as LibreOffice script

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv


TITLE = 'PyWriter v1.3'


class LoCnv(Yw7Cnv):
    """Standalone yWriter 7 converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an .yw7 file or a file of any supported type. 
            The file type determines the conversion's direction.    

        targetDoc : OdtFile
            instance of any OdtFile subclass representing the 
            odt target document. 

        sourceDoc : Novel
            instance of a Novel subclass representing the 
            html source document. 

        silentMode : bool
            True by default. Intended for automated tests. 
            If True, the GUI is not started and no further 
            user interaction is required. Overwriting of existing
            files is forced. 
            Calling scripts shall set silentMode = False.

        suffix : str
            Optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenes for a html file containing scene summaries.
            - _chapters for a html file containing chapter summaries.
    """

    def run(self, sourcePath,
            targetDoc,
            sourceDoc,
            suffix):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if sourcePath.endswith('.yw7'):
            yw7Path = sourcePath

            # Generate the target file path.

            targetDoc.filePath = sourcePath.split(
                '.yw7')[0] + suffix + '.odt'

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            message = self.yw7_to_document(yw7File, targetDoc)
            return message

        elif sourcePath.endswith(suffix + '.html'):
            sourceDoc.filePath = sourcePath

            # Determine the project file path.

            yw7Path = sourcePath.split(suffix + '.html')[0] + '.yw7'

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            message = self.document_to_yw7(sourceDoc, yw7File)
            try:
                os.remove(sourcePath)
            except:
                pass
            return message

        else:
            return 'File must be .yw7 or ' + suffix + '.odt type.'
