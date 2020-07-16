"""Import and export yWriter data. 

Standalone yWriter converter with a simple GUI

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from tkinter import *
from tkinter import messagebox

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw_new_file import YwNewFile
from pywriter.converter.yw_cnv import YwCnv


TITLE = 'yWriter import/export'


class YwCnvGui(YwCnv):
    """Standalone yWriter converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an yWriter file or a file of any supported type. 
            The file type determines the conversion's direction.    

        document : Novel
            instance of any Novel subclass representing the 
            source or target document. 

        extension : str
            File extension determining the source or target 
            document's file type. The extension is needed because 
            there can be ambiguous Novel subclasses 
            (e.g. OfficeFile).
            Examples: 
            - md
            - docx
            - odt
            - html

        silentMode : bool
            True by default. Intended for automated tests. 
            If True, the GUI is not started and no further 
            user interaction is required. Overwriting of existing
            files is forced. 
            Calling scripts shall set silentMode = False.

        suffix : str
            Optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenes for a html file containing scene summaries.
            - _chapters for a html file containing chapter summaries.
    """

    def __init__(self, sourcePath, document, silentMode=True):
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

        self._success = False

        # Run the converter.

        self.silentMode = silentMode
        self.convert(sourcePath, document)

        # Visualize the outcome.

        if not self.silentMode:

            if self._success:
                self.successInfo.config(bg='green')

            else:
                self.successInfo.config(bg='red')

            self.root.quitButton = Button(text="Quit", command=quit)
            self.root.quitButton.config(height=1, width=10)
            self.root.quitButton.pack(padx=5, pady=5)
            self.root.mainloop()

    def convert(self, sourcePath, document):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if not os.path.isfile(sourcePath):
            self.processInfo.config(text='ERROR: File not found.')

        else:
            fileName, FileExtension = os.path.splitext(sourcePath)

            if FileExtension in ['.yw5', '.yw6', '.yw7']:

                # Generate the target file path.

                document.filePath = fileName + document.SUFFIX + document.EXTENSION
                self.appInfo.config(
                    text='Export yWriter scenes content to ' + document.EXTENSION)
                self.processInfo.config(text='Project: "' + sourcePath + '"')

                # Instantiate an YwFile object and pass it along with
                # the document to the converter class.

                ywFile = YwFile(sourcePath)
                self.processInfo.config(
                    text=self.yw_to_document(ywFile, document))

            elif (document.SUFFIX == '') and (document.EXTENSIION == '.html'):
                document.filePath = sourcePath
                ywPath = sourcePath.split('.html')[0] + '.yw7'
                ywFile = YwNewFile(ywPath)

                if ywFile.file_exists():
                    self.processInfo.config(
                        text='ERROR: yWriter project already exists.')

                else:
                    self.appInfo.config(
                        text='Create a yWriter project file')
                    self.processInfo.config(
                        text='New project: "' + ywPath + '"')
                    self.processInfo.config(
                        text=self.document_to_yw(document, ywFile))

            elif sourcePath.endswith(document.SUFFIX + document.EXTENSION):
                document.filePath = sourcePath

                # Determine the project file path.

                ywPath = sourcePath.split(document.SUFFIX)[0] + '.yw7'

                if not os.path.isfile(ywPath):
                    ywPath = sourcePath.split(document.SUFFIX)[0] + '.yw6'

                    if not os.path.isfile(ywPath):
                        ywPath = sourcePath.split(document.SUFFIX)[0] + '.yw5'

                        if not os.path.isfile(ywPath):
                            ywPath = None
                            self.processInfo.config(
                                text='ERROR: No yWriter project found.')

                if ywPath:
                    self.appInfo.config(
                        text='Import yWriter scenes content from ' + document.EXTENSION)
                    self.processInfo.config(
                        text='Project: "' + ywPath + '"')

                    # Instantiate an YwFile object and pass it along with
                    # the document to the converter class.

                    ywFile = YwFile(ywPath)
                    self.processInfo.config(
                        text=self.document_to_yw(document, ywFile))

            else:
                self.processInfo.config(
                    text='ERROR: File type is not supported.')

            # Visualize the outcome.

            if self.processInfo.cget('text').startswith('SUCCESS'):
                self._success = True

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')

    def edit(self):
        pass
