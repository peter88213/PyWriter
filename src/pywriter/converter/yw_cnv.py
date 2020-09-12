"""Import and export yWriter data. 

Standalone yWriter file converter with basic error handling 

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class YwCnv():
    """Converter for yWriter project files.

    # Methods

    convert : str
        Arguments
            sourceFile : Novel
                an object representing the source file.
            targetFile : Novel
                an object representing the target file.
        Read sourceFile, merge the contents to targetFile and write targetFile.
        Return a message beginning with SUCCESS or ERROR.
        At least one sourcefile or targetFile object should be a yWriter project.

    confirm_overwrite : bool
        Arguments
            fileName : str
                Path to the file to be overwritten
        Ask for permission to overwrite the target file.
        Returns True by default.
        This method is to be overwritten by subclasses with an user interface.
    """

    def convert(self, sourceFile, targetFile):
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
