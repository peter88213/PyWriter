"""Import and export yWriter data. 

Standalone yWriter converter with a simple GUI

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *
from tkinter import messagebox

from pywriter.converter.yw_cnv import YwCnv
from pywriter.converter.file_factory import FileFactory
from pywriter.yw.yw7_new_file import Yw7NewFile


TITLE = 'yWriter import/export'


class YwCnvGui(YwCnv):
    """Standalone yWriter converter with a simple GUI. 

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

        silentMode : bool
            True by default. Intended for automated tests. 
            If True, the GUI is not started and no further 
            user interaction is required. Overwriting of existing
            files is forced. 
            Calling scripts shall set silentMode = False.

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

    edit
        Open the target file.
        To be overwritten by subclasses.
    """

    def __init__(self, sourcePath, suffix=None, silentMode=True):
        """Run the converter with a GUI. """

        # Prepare the graphical user interface.

        self.root = Tk()
        self.root.geometry("800x360")
        self.root.title(TITLE)
        self.header = Label(self.root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(self.root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.successInfo = Label(self.root)
        self.successInfo.pack(fill=X, expand=1, padx=50, pady=5)
        self.processInfo = Label(self.root, text='')
        self.processInfo.pack(padx=5, pady=5)

        self.success = False

        # Run the converter.

        self.silentMode = silentMode

        fileFactory = FileFactory()

        message, sourceFile, TargetFile = fileFactory.get_file_objects(
            sourcePath, suffix)

        if message.startswith('SUCCESS'):

            self.convert(sourceFile, TargetFile)

        else:
            self.processInfo.config(text=message)

        # Visualize the outcome.

        if not self.silentMode:

            if self.success:
                self.successInfo.config(bg='green')

            else:
                self.successInfo.config(bg='red')

            self.root.quitButton = Button(text="Quit", command=quit)
            self.root.quitButton.config(height=1, width=10)
            self.root.quitButton.pack(padx=5, pady=5)
            self.root.mainloop()

    def convert(self, sourceFile, targetFile):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if not sourceFile.file_exists():
            self.processInfo.config(text='ERROR: File not found.')

        else:
            if sourceFile.EXTENSION in ['.yw5', '.yw6', '.yw7']:

                self.appInfo.config(
                    text='Export yWriter project data to ' + targetFile.EXTENSION)
                self.processInfo.config(
                    text='Project: "' + sourceFile.filePath + '"')
                self.processInfo.config(
                    text=YwCnv.convert(self, sourceFile, targetFile))

            elif isinstance(targetFile, Yw7NewFile):

                if targetFile.file_exists():
                    self.processInfo.config(
                        text='ERROR: "' + targetFile._filePath + '" already exists.')

                else:
                    self.appInfo.config(
                        text='Create a yWriter project file')
                    self.processInfo.config(
                        text='New project: "' + targetFile.filePath + '"')
                    self.processInfo.config(
                        text=YwCnv.convert(self, sourceFile, targetFile))

            else:

                self.appInfo.config(
                    text='Import yWriter project data from ' + sourceFile.EXTENSION)
                self.processInfo.config(
                    text='Project: "' + targetFile.filePath + '"')
                self.processInfo.config(
                    text=YwCnv.convert(self, sourceFile, targetFile))

            # Visualize the outcome.

            if self.processInfo.cget('text').startswith('SUCCESS'):
                self.success = True

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')

    def edit(self):
        pass
