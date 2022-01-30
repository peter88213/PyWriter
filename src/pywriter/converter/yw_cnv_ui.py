"""Provide a class for Novel file conversion with user interface.

All converters with a user interface inherit from this class. 

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import webbrowser

from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui
from pywriter.converter.yw_cnv import YwCnv


class YwCnvUi(YwCnv):
    """Base class for Novel file conversion with user interface.

    Public methods:
        export_from_yw(sourceFile, targetFile) -- Convert from yWriter project to other file format.
        import_to_yw(sourceFile, targetFile) -- Convert from any file format to yWriter project.
        confirm_overwrite(fileName) -- Return boolean permission to overwrite the target file.

    Instance variables:
        ui -- Ui (can be overridden e.g. by subclasses).
        newFile -- string; path to the target file in case of success.   
    """

    def __init__(self):
        """Define instance variables."""
        self.ui = Ui('')
        # Per default, 'silent mode' is active.

        self.newFile = None
        # Also indicates successful conversion.

    def export_from_yw(self, sourceFile, targetFile):
        """Convert from yWriter project to other file format.

        sourceFile -- YwFile subclass instance.
        targetFile -- Any Novel subclass instance.

        This is a primitive operation of the run() template method.

        1. Send specific information about the conversion to the UI.
        2. Convert sourceFile into targetFile.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """

        # Send specific information about the conversion to the UI.

        self.ui.set_info_what(
            f'Input: {sourceFile.DESCRIPTION} "{os.path.normpath(sourceFile.filePath)}"\nOutput: {targetFile.DESCRIPTION} "{os.path.normpath(targetFile.filePath)}"')

        # Convert sourceFile into targetFile.

        message = self.convert(sourceFile, targetFile)

        # Pass the message to the UI.

        self.ui.set_info_how(message)

        # Save the new file pathname.

        if message.startswith(ERROR):
            self.newFile = None

        else:
            self.newFile = targetFile.filePath

    def create_yw7(self, sourceFile, targetFile):
        """Create targetFile from sourceFile.

        sourceFile -- Any Novel subclass instance.
        targetFile -- YwFile subclass instance.

        This is a primitive operation of the run() template method.

        1. Send specific information about the conversion to the UI.
        2. Convert sourceFile into targetFile.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - Tf targetFile already exists as a file, the conversion is cancelled,
          an error message is sent to the UI.
        - If the conversion fails, newFile is set to None.
        """

        # Send specific information about the conversion to the UI.

        self.ui.set_info_what(
            f'Create a yWriter project file from {sourceFile.DESCRIPTION}\nNew project: "{os.path.normpath(targetFile.filePath)}"')

        if os.path.isfile(targetFile.filePath):
            self.ui.set_info_how(f'{ERROR}"{os.path.normpath(targetFile.filePath)}" already exists.')

        else:
            # Convert sourceFile into targetFile.

            message = self.convert(sourceFile, targetFile)

            # Pass the message to the UI.

            self.ui.set_info_how(message)

            # Save the new file pathname.

            if message.startswith(ERROR):
                self.newFile = None

            else:
                self.newFile = targetFile.filePath

    def import_to_yw(self, sourceFile, targetFile):
        """Convert from any file format to yWriter project.

        sourceFile -- Any Novel subclass instance.
        targetFile -- YwFile subclass instance.

        This is a primitive operation of the run() template method.

        1. Send specific information about the conversion to the UI.
        2. Convert sourceFile into targetFile.
        3. Pass the message to the UI.
        4. Delete the temporay file, if exists.
        5. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """

        # Send specific information about the conversion to the UI.

        self.ui.set_info_what(
            f'Input: {sourceFile.DESCRIPTION} "{os.path.normpath(sourceFile.filePath)}"\nOutput: {targetFile.DESCRIPTION} "{os.path.normpath(targetFile.filePath)}"')

        # Convert sourceFile into targetFile.

        message = self.convert(sourceFile, targetFile)

        # Pass the message to the UI.

        self.ui.set_info_how(message)

        # Delete the temporay file, if exists.

        self.delete_tempfile(sourceFile.filePath)

        # Save the new file pathname.

        if message.startswith(ERROR):
            self.newFile = None

        else:
            self.newFile = targetFile.filePath

    def confirm_overwrite(self, filePath):
        """Return boolean permission to overwrite the target file, overriding the superclass method."""
        return self.ui.ask_yes_no(f'Overwrite existing file "{os.path.normpath(filePath)}"?')

    def delete_tempfile(self, filePath):
        """Delete filePath if it is a temporary file no longer needed."""

        if filePath.endswith('.html'):
            # Might it be a temporary text document?

            if os.path.isfile(filePath.replace('.html', '.odt')):
                # Does a corresponding Office document exist?

                try:
                    os.remove(filePath)

                except:
                    pass

        elif filePath.endswith('.csv'):
            # Might it be a temporary spreadsheet document?

            if os.path.isfile(filePath.replace('.csv', '.ods')):
                # Does a corresponding Office document exist?

                try:
                    os.remove(filePath)

                except:
                    pass

    def open_newFile(self):
        """Open the converted file for editing and exit the converter script."""
        webbrowser.open(self.newFile)
        sys.exit(0)
