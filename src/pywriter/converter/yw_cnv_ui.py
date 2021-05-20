"""Provide a class for Novel file conversion with user interface.

User interface-specific converters inherit from this class. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys

from pywriter.ui.ui import Ui
from pywriter.converter.yw_cnv import YwCnv

from pywriter.converter.file_factory import FileFactory
from pywriter.converter.export_source_factory import ExportSourceFactory
from pywriter.converter.export_target_factory import ExportTargetFactory
from pywriter.converter.import_source_factory import ImportSourceFactory
from pywriter.converter.import_target_factory import ImportTargetFactory


class YwCnvUi(YwCnv):
    """Class for Novel file conversion with user interface.

    Public methods:
    run(sourcePath, suffix) -- Create source and target objects and run conversion.

    All converters with a user interface inherit from this class. 
    """

    EXPORT_SOURCE_CLASSES = []
    EXPORT_TARGET_CLASSES = []
    IMPORT_SOURCE_CLASSES = []
    IMPORT_TARGET_CLASSES = []

    def __init__(self):
        """Define instance variables.

        ui -- user interface object; instance of Ui or a Ui subclass.
        fileFactory -- file factory object; instance of a FileFactory subclass.
        """

        self.ui = Ui('')
        # Per default, 'silent mode' is active.

        self.exportSourceFactory = ExportSourceFactory(
            self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(
            self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(
            self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(
            self.IMPORT_TARGET_CLASSES)
        self.newProjectFactory = FileFactory()

        self.newFile = None
        # Also indicates successful conversion.

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        sourcePath -- str; the source file path.
        suffix -- str; target file name suffix. 

        This is a template method that calls primitive operations by case.
        """
        if not os.path.isfile(sourcePath):
            self.ui.set_info_how(
                'ERROR: File "' + os.path.normpath(sourcePath) + '" not found.')
            return

        message, sourceFile, dummy = self.exportSourceFactory.make_file_objects(
            sourcePath, **kwargs)

        if message.startswith('SUCCESS'):
            # The source file is a yWriter project.

            message, dummy, targetFile = self.exportTargetFactory.make_file_objects(
                sourcePath, **kwargs)

            if message.startswith('SUCCESS'):
                self.export_from_yw(sourceFile, targetFile)

            else:
                self.ui.set_info_how(message)

        else:
            # The source file is not a yWriter project.

            message, sourceFile, dummy = self.importSourceFactory.make_file_objects(
                sourcePath, **kwargs)

            if message.startswith('SUCCESS'):
                kwargs['suffix'] = sourceFile.SUFFIX
                message, dummy, targetFile = self.importTargetFactory.make_file_objects(
                    sourcePath, **kwargs)

                if message.startswith('SUCCESS'):
                    self.import_to_yw(sourceFile, targetFile)

                else:
                    self.ui.set_info_how(message)

            else:
                # A new yWriter project might be required.

                message, sourceFile, targetFile = self.newProjectFactory.make_file_objects(
                    sourcePath, **kwargs)

                if message.startswith('SUCCESS'):
                    self.create_yw7(sourceFile, targetFile)

                else:
                    self.ui.set_info_how(message)

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

        self.ui.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')

        # Convert sourceFile into targetFile.

        message = self.convert(sourceFile, targetFile)

        # Pass the message to the UI.

        self.ui.set_info_how(message)

        # Save the new file pathname.

        if message.startswith('SUCCESS'):
            self.newFile = targetFile.filePath

        else:
            self.newFile = None

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
            'Create a yWriter project file from ' + sourceFile.DESCRIPTION + '\nNew project: "' + os.path.normpath(targetFile.filePath) + '"')

        if targetFile.file_exists():
            self.ui.set_info_how(
                'ERROR: "' + os.path.normpath(targetFile.filePath) + '" already exists.')

        else:
            # Convert sourceFile into targetFile.

            message = self.convert(sourceFile, targetFile)

            # Pass the message to the UI.

            self.ui.set_info_how(message)

            # Save the new file pathname.

            if message.startswith('SUCCESS'):
                self.newFile = targetFile.filePath

            else:
                self.newFile = None

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

        self.ui.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')

        # Convert sourceFile into targetFile.

        message = self.convert(sourceFile, targetFile)

        # Pass the message to the UI.

        self.ui.set_info_how(message)

        # Delete the temporay file, if exists.

        self.delete_tempfile(sourceFile.filePath)

        # Save the new file pathname.

        if message.startswith('SUCCESS'):
            self.newFile = targetFile.filePath

        else:
            self.newFile = None

    def confirm_overwrite(self, filePath):
        """Return boolean permission to overwrite the target file, overriding the superclass method."""
        return self.ui.ask_yes_no('Overwrite existing file "' + os.path.normpath(filePath) + '"?')

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
        os.startfile(self.newFile)
        sys.exit(0)
