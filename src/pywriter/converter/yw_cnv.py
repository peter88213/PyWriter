"""Import and export yWriter data. 

Standalone yWriter file converter with basic error handling 

Copyright (c) 2019, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class YwCnv():
    """Converter for yWriter project files.

    # Methods

    yw_to_document : str
        Arguments
            ywFile : YwFile
                an object representing the source file.
            documentFile : Novel
                a Novel subclass instance representing the target file.
        Read yWriter file, parse xml and create a document file.
        Return a message beginning with SUCCESS or ERROR.    

    document_to_yw : str
        Arguments
            documentFile : Novel
                a Novel subclass instance representing the source file.
            ywFile : YwFile
                an object representing the target file.
        Read document file, convert its content to xml, and replace yWriter file.
        Return a message beginning with SUCCESS or ERROR.

    confirm_overwrite : bool
        Arguments
            fileName : str
                Path to the file to be overwritten
        Ask for permission to overwrite the target file.
        Returns True by default.
        This method is to be overwritten by subclasses with an user interface.
    """

    def yw_to_document(self, ywFile, documentFile):
        """Read yWriter file and convert xml to a document file."""
        if ywFile.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        if ywFile.filePath is None:
            return 'ERROR: "' + ywFile.filePath + '" is not an yWriter project.'

        message = ywFile.read()

        if message.startswith('ERROR'):
            return message

        if documentFile.file_exists():

            if not self.confirm_overwrite(documentFile.filePath):
                return 'Program abort by user.'

        return documentFile.write(ywFile)

    def document_to_yw(self, documentFile, ywFile):
        """Read document file, convert its content to xml, and replace yWriter file."""
        if ywFile.is_locked():
            return 'ERROR: yWriter seems to be open. Please close first.'

        if ywFile.filePath is None:
            return 'ERROR: "' + ywFile.filePath + '" is not an yWriter project.'

        if not ywFile.file_exists():
            return 'ERROR: Project "' + ywFile.filePath + '" not found.'

        if not self.confirm_overwrite(ywFile.filePath):
            return 'Program abort by user.'

        if documentFile.filePath is None:
            return 'ERROR: "' + documentFile.filePath + '" is not of the supported type.'

        if not documentFile.file_exists():
            return 'ERROR: "' + documentFile.filePath + '" not found.'

        message = documentFile.read()

        if message.startswith('ERROR'):
            return message

        message = ywFile.read()
        # initialize ywFile data

        if message.startswith('ERROR'):
            return message

        prjStructure = documentFile.get_structure()

        if prjStructure is not None:

            if prjStructure == '':
                return 'ERROR: Source file contains no yWriter project structure information.'

            if prjStructure != ywFile.get_structure():
                return 'ERROR: Structure mismatch - yWriter project not modified.'

        return ywFile.write(documentFile)

    def confirm_overwrite(self, fileName):
        """To be overwritten by subclasses with UI."""
        return True
