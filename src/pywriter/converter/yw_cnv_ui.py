"""Import and export yWriter data. 

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.cnv_ui import CnvUi
from pywriter.converter.yw_cnv import YwCnv
from pywriter.converter.file_factory import FileFactory
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator


class YwCnvUi(YwCnv):
    """Standalone yWriter converter with a simple tkinter GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an yWriter file or a file of any supported type. 
            The file type determines the conversion's direction.    

        suffix : str
            Optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenes for a html file containing scene summaries.
            - _chapters for a html file containing chapter summaries.

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

    """

    def __init__(self, sourcePath, suffix=None):
        """Run the converter with a GUI. """

        fileFactory = FileFactory()

        # Initialize the GUI

        self.cnvUi = CnvUi('yWriter import/export')

        # Run the converter.

        self.success = False
        message, sourceFile, TargetFile = fileFactory.get_file_objects(
            sourcePath, suffix)

        if message.startswith('SUCCESS'):
            self.convert(sourceFile, TargetFile)

        else:
            self.cnvUi.set_info_how(message)

    def convert(self, sourceFile, targetFile):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if not sourceFile.file_exists():
            self.cnvUi.set_info_how(
                'ERROR: File "' + os.path.normpath(sourceFile.filePath) + '" not found.')

        else:
            if sourceFile.EXTENSION in self.YW_EXTENSIONS:

                self.cnvUi.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
                    sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
                self.cnvUi.set_info_how(
                    YwCnv.convert(self, sourceFile, targetFile))

            elif isinstance(targetFile.ywTreeBuilder, Yw7TreeCreator):

                if targetFile.file_exists():
                    self.cnvUi.set_info_how(
                        'ERROR: "' + os.path.normpath(targetFile._filePath) + '" already exists.')

                else:
                    self.cnvUi.set_info_what(
                        'Create a yWriter project file from ' + sourceFile.DESCRIPTION)
                    self.cnvUi.set_info_how(
                        'New project: "' + os.path.normpath(targetFile.filePath) + '"')
            else:

                self.cnvUi.set_info_what('Input: ' + sourceFile.DESCRIPTION + ' "' + os.path.normpath(
                    sourceFile.filePath) + '"\nOutput: ' + targetFile.DESCRIPTION + ' "' + os.path.normpath(targetFile.filePath) + '"')
                self.cnvUi.set_info_how(
                    YwCnv.convert(self, sourceFile, targetFile))

            # Visualize the outcome.

            if self.cnvUi.get_info_how().startswith('SUCCESS'):
                self.success = True

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """
        return self.cnvUi.ask_yes_no('Overwrite existing file "' + os.path.normpath(filePath) + '"?')
