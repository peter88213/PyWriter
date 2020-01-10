"""Import and export yWriter 7 data. 

Standalone converter with a simple GUI

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from tkinter import *
from tkinter import messagebox

from pywriter.convert.yw7cnv import Yw7Cnv
from pywriter.model.yw7file import Yw7File


TITLE = 'PyWriter v1.2'


class CnvRunner(Yw7Cnv):

    def __init__(self, sourcePath, document, extension, silentMode=True, suffix=''):
        """File conversion for proofreading """
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

        self.silentMode = silentMode

        self.run(sourcePath, document, extension, suffix)

        if not self.silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.config(height=1, width=10)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def run(self, sourcePath, document, extension, suffix):
        """File conversion for editing """

        if sourcePath.endswith('.yw7'):
            yw7Path = sourcePath
            document.filePath = sourcePath.split(
                '.yw7')[0] + suffix + '.' + extension
            self.appInfo.config(
                text='Export yWriter7 scenes content to html')
            self.processInfo.config(text='Project: "' + yw7Path + '"')

            yw7File = Yw7File(yw7Path)

            self.processInfo.config(
                text=self.yw7_to_document(yw7File, document))

        elif sourcePath.endswith(suffix + '.' + extension):
            document.filePath = sourcePath
            yw7Path = sourcePath.split(suffix + '.' + extension)[0] + '.yw7'
            self.appInfo.config(
                text='Import yWriter7 scenes content from html')
            self.processInfo.config(
                text='Proofed scenes in "' + document.filePath + '"')

            yw7File = Yw7File(yw7Path)

            self.processInfo.config(
                text=self.document_to_yw7(document, yw7File))

        else:
            self.processInfo.config(
                text='Argument is wrong or missing (drag and drop error?)\nInput file must be .yw7 or ' + suffix + '.' + extension + ' type.')
            self.successInfo.config(bg='red')

        if 'ERROR' in self.processInfo.cget('text'):
            self.successInfo.config(bg='red')

        elif 'SUCCESS' in self.processInfo.cget('text'):
            self.successInfo.config(bg='green')

    def confirm_overwrite(self, file):
        """ Invoked by subclass if file already exists. """

        if self.silentMode:
            return(True)

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + file + '"?')
