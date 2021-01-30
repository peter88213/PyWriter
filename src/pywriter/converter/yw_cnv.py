"""Import and export yWriter data. 

Standalone yWriter file converter with basic error handling 

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class YwCnv():
    """Converter for yWriter project files.
    """

    def convert(self, sourceFile, targetFile):
        """Read the source file, merge its content with that of the target,
        and write the result to the target file.
        Return a message beginning with SUCCESS or ERROR.
        """

        if sourceFile.filePath is None:
            return 'ERROR: Source "' + os.path.normpath(sourceFile.filePath) + '" is not of the supported type.'

        if not sourceFile.file_exists():
            return 'ERROR: "' + os.path.normpath(sourceFile.filePath) + '" not found.'

        if targetFile.filePath is None:
            return 'ERROR: Target "' + os.path.normpath(targetFile.filePath) + '" is not of the supported type.'

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
        """Hook for subclasses with UI."""
        return True
