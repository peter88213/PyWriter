"""Modules for conversion of Novel subclasses.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class YwCnv():
    """Base class for Novel file conversion.

    Public methods:
    convert(sourceFile, targetFile) -- Convert sourceFile into targetFile and return a message.

    All converters inherit from this class. 
    """

    def convert(self, sourceFile, targetFile):
        """Convert sourceFile into targetFile and return a message.

        sourceFile, targetFile -- Novel subclass instances.

        1. Make the source object read the source file.
        2. Make the target object merge the source object's instance variables.
        3. Make the target object write the target file.
        Return a message beginning with SUCCESS or ERROR.

        Error handling:
        - Check if sourceFile and targetFile are correctly initialized.
        - Ask for permission to overwrite targetFile.
        - Pass the error messages of the called methods of sourceFile and targetFile.
        - The success message comes from targetFile.write(), if called.       
        """

        # Initial error handling.

        if sourceFile.filePath is None:
            return 'ERROR: Source "' + os.path.normpath(sourceFile.filePath) + '" is not of the supported type.'

        if not sourceFile.file_exists():
            return 'ERROR: "' + os.path.normpath(sourceFile.filePath) + '" not found.'

        if targetFile.filePath is None:
            return 'ERROR: Target "' + os.path.normpath(targetFile.filePath) + '" is not of the supported type.'

        if targetFile.file_exists() and not self.confirm_overwrite(targetFile.filePath):
            return 'ERROR: Action canceled by user.'

        # Make the source object read the source file.

        message = sourceFile.read()

        if message.startswith('ERROR'):
            return message

        # Make the target object merge the source object's instance variables.

        message = targetFile.merge(sourceFile)

        if message.startswith('ERROR'):
            return message

        # Make the source object write the target file.

        return targetFile.write()

    def confirm_overwrite(self, fileName):
        """Return boolean permission to overwrite the target file."""
        return True
