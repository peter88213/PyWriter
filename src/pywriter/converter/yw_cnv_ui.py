"""Provide a class for Novel file conversion with user interface.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys

from pywriter.ui.ui import Ui
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator


class YwCnvUi(YwCnv):
    """Class for Novel file conversion with user interface.



    """

    YW_EXTENSIONS = ['.yw5', '.yw6', '.yw7']

    def __init__(self):
        """Define instance variables.

        ui -- The user interface; Ui or a Ui subclass.
        fileFactory -- The file factory; 
        """
        self.ui = Ui('')
        # Per default, 'silent mode' is active.

        self.fileFactory = None
        # Must be set explicitly from outside.

        self.newFile = None
        # Also indicates successful conversion.

    def run(self, sourcePath, suffix=None):
        """Create source and target objects and run conversion.
        """
        message, sourceFile, targetFile = self.fileFactory.get_file_objects(
            sourcePath, suffix)

        if not message.startswith('SUCCESS'):
            self.ui.set_info_how(message)

        elif not sourceFile.file_exists():
            self.ui.set_info_how(
                'ERROR: File "' + os.path.normpath(sourceFile.filePath) + '" not found.')

        elif sourceFile.EXTENSION in self.YW_EXTENSIONS:
            self.export_from_yw(sourceFile, targetFile)

        elif isinstance(targetFile.ywTreeBuilder, Yw7TreeCreator):
            self.create_yw7(sourceFile, targetFile)

        else:
            self.import_to_yw(sourceFile, targetFile)

    def export_from_yw(self, sourceFile, targetFile):
        """Convert from yWriter project to other file format. 


        Pass info and messages to ui.
        Set newFile
        """
        self.ui.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
        message = self.convert(sourceFile, targetFile)
        self.ui.set_info_how(message)

        if message.startswith('SUCCESS'):
            self.newFile = targetFile.filePath

    def create_yw7(self, sourceFile, targetFile):
        """Template method for creation of a new yw7 project.
        """
        self.ui.set_info_what(
            'Create a yWriter project file from ' + sourceFile.DESCRIPTION + '\nNew project: "' + os.path.normpath(targetFile.filePath) + '"')

        if targetFile.file_exists():
            self.ui.set_info_how(
                'ERROR: "' + os.path.normpath(targetFile.filePath) + '" already exists.')

        else:
            message = self.convert(sourceFile, targetFile)
            self.ui.set_info_how(message)

            if message.startswith('SUCCESS'):
                self.newFile = targetFile.filePath

    def import_to_yw(self, sourceFile, targetFile):
        """Convert any file format into yWriter project. Pass info and messages to ui."""
        self.ui.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
        message = self.convert(sourceFile, targetFile)
        self.ui.set_info_how(message)
        self.delete_tempfile(sourceFile.filePath)

        if message.startswith('SUCCESS'):
            self.newFile = targetFile.filePath

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
        os.startfile(self.newFile)
        sys.exit(0)
