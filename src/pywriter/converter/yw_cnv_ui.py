"""Import and export yWriter data. 

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.ui import Ui
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator


class YwCnvUi(YwCnv):
    """Standalone yWriter converter with a 'silent' user interface. 
    """

    YW_EXTENSIONS = ['.yw5', '.yw6', '.yw7']

    def __init__(self):
        self.userInterface = Ui('yWriter import/export')
        self.success = False
        self.fileFactory = None

    def run(self, sourcePath, suffix=None):
        """Create source and target objects and run conversion.
        """
        message, sourceFile, targetFile = self.fileFactory.get_file_objects(
            sourcePath, suffix)

        if not message.startswith('SUCCESS'):
            self.userInterface.set_info_how(message)

        elif not sourceFile.file_exists():
            self.userInterface.set_info_how(
                'ERROR: File "' + os.path.normpath(sourceFile.filePath) + '" not found.')

        elif sourceFile.EXTENSION in self.YW_EXTENSIONS:
            self.export_from_yw(sourceFile, targetFile)

        elif isinstance(targetFile.ywTreeBuilder, Yw7TreeCreator):
            self.create_yw7(sourceFile, targetFile)

        else:
            self.import_to_yw(sourceFile, targetFile)

        self.finish(sourcePath)

    def export_from_yw(self, sourceFile, targetFile):
        """Template method for conversion from yw to other.
        """
        self.userInterface.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
        message = self.convert(sourceFile, targetFile)
        self.userInterface.set_info_how(message)

        if message.startswith('SUCCESS'):
            self.success = True

    def create_yw7(self, sourceFile, targetFile):
        """Template method for creation of a new yw7 project.
        """
        self.userInterface.set_info_what(
            'Create a yWriter project file from ' + sourceFile.DESCRIPTION + '\nNew project: "' + os.path.normpath(targetFile.filePath) + '"')

        if targetFile.file_exists():
            self.userInterface.set_info_how(
                'ERROR: "' + os.path.normpath(targetFile.filePath) + '" already exists.')

        else:
            message = self.convert(sourceFile, targetFile)
            self.userInterface.set_info_how(message)

            if message.startswith('SUCCESS'):
                self.success = True

    def import_to_yw(self, sourceFile, targetFile):
        """Template method for conversion from other to yw.
        """
        self.userInterface.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
        message = self.convert(sourceFile, targetFile)
        self.userInterface.set_info_how(message)

        if message.startswith('SUCCESS'):
            self.success = True

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists.
        """
        return self.userInterface.ask_yes_no('Overwrite existing file "' + os.path.normpath(filePath) + '"?')

    def delete_tempfile(self, filePath):
        """If an Office file exists, delete the temporary file."""

        if filePath.endswith('.html'):

            if os.path.isfile(filePath.replace('.html', '.odt')):

                try:
                    os.remove(filePath)

                except:
                    pass

        elif filePath.endswith('.csv'):

            if os.path.isfile(filePath.replace('.csv', '.ods')):

                try:
                    os.remove(filePath)

                except:
                    pass

    def finish(self, sourcePath):
        """Hook for actions to take place after the conversion."""
