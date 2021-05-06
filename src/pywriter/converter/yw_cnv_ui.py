"""Import and export yWriter data. 

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
    """yWriter converter using a user interface facade. 
    Per default, 'silent mode' is active.
    """

    YW_EXTENSIONS = ['.yw5', '.yw6', '.yw7']

    def __init__(self):
        self.ui = Ui('')
        self.fileFactory = None
        self.newFile = None

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
        """Template method for conversion from yw to other.
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
        """Template method for conversion from other to yw.
        """
        self.ui.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
            sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
        message = self.convert(sourceFile, targetFile)
        self.ui.set_info_how(message)
        self.delete_tempfile(sourceFile.filePath)

        if message.startswith('SUCCESS'):
            self.newFile = targetFile.filePath

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists.
        """
        return self.ui.ask_yes_no('Overwrite existing file "' + os.path.normpath(filePath) + '"?')

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

    def open_newFile(self):
        os.startfile(self.newFile)
        sys.exit(0)
