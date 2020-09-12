"""Import and export yWriter data. 

Standalone yWriter file converter with basic error handling 

Copyright (c) 2020 Peter Triesberger
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

    def yw_to_document(self, sourceFile, targetFile):
        """Read yWriter file and convert xml to a document file."""

        return self.document_to_yw(sourceFile, targetFile)

    def document_to_yw(self, sourceFile, targetFile):
        """Read document file, convert its content to xml, and replace yWriter file."""

        if sourceFile.filePath is None:
            return 'ERROR: "' + sourceFile.filePath + '" is not of the supported type.'

        if not sourceFile.file_exists():
            return 'ERROR: "' + sourceFile.filePath + '" not found.'

        if targetFile.filePath is None:
            return 'ERROR: "' + targetFile.filePath + '" is not of the supported type.'

        if targetFile.file_exists() and not self.confirm_overwrite(targetFile.filePath):
            return 'Program abort by user.'

        message = sourceFile.read()

        if message.startswith('ERROR'):
            return message

        message = targetFile.merge(sourceFile)

        if message.startswith('ERROR'):
            return message

        return targetFile.write()

    def confirm_overwrite(self, fileName):
        """To be overwritten by subclasses with UI."""
        return True
