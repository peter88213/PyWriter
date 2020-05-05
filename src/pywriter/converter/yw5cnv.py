"""Import and export yWriter 5 data. 

Standalone yWriter 5 file converter with basic error handling 

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Yw5Cnv():
    """Converter for yWriter 5 project files.

    # Methods

    yw_to_document : str
        Arguments
            yw5File : Yw5File
                an object representing the source file.
            documentFile : Novel
                a Novel subclass instance representing the target file.
        Read .yw5 file, parse xml and create a document file.
        Return a message beginning with SUCCESS or ERROR.    

    document_to_yw5 : str
        Arguments
            documentFile : Novel
                a Novel subclass instance representing the source file.
            yw5File : Yw5File
                an object representing the target file.
        Read document file, convert its content to xml, and replace .yw5 file.
        Return a message beginning with SUCCESS or ERROR.

    confirm_overwrite : bool
        Arguments
            fileName : str
                Path to the file to be overwritten
        Ask for permission to overwrite the target file.
        Returns True by default.
        This method is to be overwritten by subclasses with an user interface.
    """

    def yw5_to_document(self, yw5File, documentFile):
        """Read .yw5 file and convert xml to a document file."""
        if yw5File.is_locked():
            return 'ERROR: yWriter 5 seems to be open. Please close first.'

        if yw5File.filePath is None:
            return 'ERROR: "' + yw5File.filePath + '" is not an yWriter 5 project.'

        message = yw5File.read()

        if message.startswith('ERROR'):
            return message

        if documentFile.file_exists():

            if not self.confirm_overwrite(documentFile.filePath):
                return 'Program abort by user.'

        return documentFile.write(yw5File)

    def document_to_yw5(self, documentFile, yw5File):
        """Read document file, convert its content to xml, and replace .yw5 file."""
        if yw5File.is_locked():
            return 'ERROR: yWriter 5 seems to be open. Please close first.'

        if yw5File.filePath is None:
            return 'ERROR: "' + yw5File.filePath + '" is not an yWriter 5 project.'

        if not yw5File.file_exists():
            return 'ERROR: Project "' + yw5File.filePath + '" not found.'

        if not self.confirm_overwrite(yw5File.filePath):
            return 'Program abort by user.'

        if documentFile.filePath is None:
            return 'ERROR: "' + documentFile.filePath + '" is not of the supported type.'

        if not documentFile.file_exists():
            return 'ERROR: "' + documentFile.filePath + '" not found.'

        message = documentFile.read()

        if message.startswith('ERROR'):
            return message

        message = yw5File.read()
        # initialize yw5File data

        if message.startswith('ERROR'):
            return message

        prjStructure = documentFile.get_structure()

        if prjStructure is not None:

            if prjStructure == '':
                return 'ERROR: Source file contains no yWriter project structure information.'

            if prjStructure != yw5File.get_structure():
                return 'ERROR: Structure mismatch - yWriter project not modified.'

        return yw5File.write(documentFile)

    def confirm_overwrite(self, fileName):
        """To be overwritten by subclasses with UI."""
        return True
