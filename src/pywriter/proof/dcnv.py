"""Import and export ywriter7 scenes for proofing.

Proof reading Office document

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.proof.officefile import OfficeFile
from pywriter.core.yw7file import Yw7File


class DCnv():
    """

    # Attributes

    # Methods

    """

    def __init__(self, yw7Path, documentPath):
        self.yw7Path = yw7Path
        self.yw7File = Yw7File(self.yw7Path)
        self.documentPath = documentPath
        self.documentFile = OfficeFile(self.documentPath)

    def yw7_to_document(self):
        """Read .yw7 file and convert sceneContents to html. """

        if self.yw7File.is_locked():
            return('ERROR: "' + self.yw7Path + '" seems to be locked. Please close yWriter 7.')

        if self.yw7File.filePath is None:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_exists():
            return('ERROR: Project "' + self.yw7Path + '" not found.')

        message = self.yw7File.read()

        if message.startswith('ERROR'):
            return(message)

        if self.documentFile.file_exists():

            if not self.confirm_overwrite(self.documentPath):
                return('Program abort by user.')

        return(self.documentFile.write(self.yw7File))

    def document_to_yw7(self):
        """Convert html into yw7 newContents and modify .yw7 file. """

        if self.yw7File.is_locked():
            return('ERROR: "' + self.yw7Path + '" seems to be locked. Please close yWriter 7.')

        if self.yw7File.filePath is None:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_exists():
            return('ERROR: Project "' + self.yw7Path + '" not found.')

        elif not self.confirm_overwrite(self.yw7Path):
            return('Program abort by user.')

        if self.documentFile.filePath is None:
            return('ERROR: "' + self.documentPath + '" is not an Office file.')

        if not self.documentFile.file_exists():
            return('ERROR: "' + self.documentPath + '" not found.')

        message = self.documentFile.read()

        if message.startswith('ERROR'):
            return(message)

        message = self.yw7File.read()

        if message.startswith('ERROR'):
            return(message)

        prjStructure = self.documentFile.get_structure()

        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        return(self.yw7File.write(self.documentFile))

    def confirm_overwrite(self, fileName):
        return(True)
