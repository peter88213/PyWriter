"""Import and export yWriter 7 data. 

Standalone yWriter 7 converter with a simple GUI

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from tkinter import *
from tkinter import messagebox

from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv


TITLE = 'PyWriter v1.3'


class HybridCnv(Yw7Cnv):
    """Standalone yWriter 7 converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an .yw7 file or a file of any supported type. 
            The file type determines the conversion's direction.    

        targetDoc : OdtFile
            instance of any OdtFile subclass representing the 
            odt target document. 

        sourceDoc : Novel
            instance of a Novel subclass representing the 
            html source document. 

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

    def __init__(self, sourcePath,
                 targetDoc,
                 sourceDoc,
                 silentMode=True,
                 suffix=''):
        """Run the converter with a GUI. """

        # Prepare the graphical user interface.

        root = Tk()
        root.geometry("800x300")
        root.title(TITLE)
        self.header = Label(root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.successInfo = Label(root)
        self.successInfo.pack(fill=X, expand=1, padx=50, pady=5)
        self.processInfo = Label(root, text='')
        self.processInfo.pack(padx=5, pady=5)

        # Run the converter.

        self.silentMode = silentMode
        self.__run(sourcePath, targetDoc, sourceDoc, suffix)

        # Visualize the outcome.

        if not self.silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.config(height=1, width=10)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def __run(self, sourcePath,
              targetDoc,
              sourceDoc,
              suffix):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if sourcePath.endswith('.yw7'):
            yw7Path = sourcePath

            # Generate the target file path.

            targetDoc.filePath = sourcePath.split(
                '.yw7')[0] + suffix + '.odt'
            self.appInfo.config(
                text='Export yWriter7 scenes content to odt')
            self.processInfo.config(text='Project: "' + yw7Path + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.yw7_to_document(yw7File, targetDoc))

        elif sourcePath.endswith(suffix + '.html'):
            sourceDoc.filePath = sourcePath

            # Determine the project file path.

            yw7Path = sourcePath.split(suffix + '.html')[0] + '.yw7'
            self.appInfo.config(
                text='Import yWriter7 scenes content from html')
            self.processInfo.config(
                text='Proofed scenes in "' + sourceDoc.filePath + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.document_to_yw7(sourceDoc, yw7File))

        else:
            self.processInfo.config(
                text='Argument is wrong or missing (drag and drop error?)\nInput file must be .yw7 or ' + suffix + '.html type.')
            self.successInfo.config(bg='red')

        # Visualize the outcome.

        if 'ERROR' in self.processInfo.cget('text'):
            self.successInfo.config(bg='red')

        elif 'SUCCESS' in self.processInfo.cget('text'):
            self.successInfo.config(bg='green')

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')
