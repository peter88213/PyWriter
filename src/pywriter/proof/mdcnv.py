"""PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Yw7Cnv():

    def yw7_to_document(self, yw7File, documentFile):
        """Read .yw7 file and convert xml to markdown. """

        if yw7File.is_locked():
            return('ERROR: "' + yw7File.filePath + '" seems to be locked. Please close yWriter 7.')

        if yw7File.filePath is None:
            return('ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.')

        message = yw7File.read()
        if message.startswith('ERROR'):
            return(message)

        return(documentFile.write(yw7File))

    def document_to_yw7(self, documentFile, yw7File):
        """Convert markdown to xml and replace .yw7 file. """

        if yw7File.is_locked():
            return('ERROR: "' + yw7File.filePath + '" seems to be locked. Please close yWriter 7.')

        if yw7File.filePath is None:
            return('ERROR: "' + yw7File.filePath + '" is not an yWriter 7 project.')

        if not yw7File.file_exists():
            return('ERROR: Project "' + yw7File.filePath + '" not found.')
        else:
            if not self.confirm_overwrite(yw7File.filePath):
                return('Program abort by user.')

        if documentFile.filePath is None:
            return('ERROR: "' + documentFile.filePath + '" is not a Markdown file.')

        if not documentFile.file_exists():
            return('ERROR: "' + documentFile.filePath + '" not found.')

        message = documentFile.read()
        if message.startswith('ERROR'):
            return(message)

        prjStructure = documentFile.get_structure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        message = yw7File.read()
        if message.startswith('ERROR'):
            return(message)

        if prjStructure != yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        return(yw7File.write(documentFile))

    def confirm_overwrite(self, fileName):
        return(True)
