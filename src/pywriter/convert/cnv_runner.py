"""Import and export ywriter7 scenes for proofing. 

Proof reading file with visible chapter and scene tags.

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from tkinter import *
from tkinter import messagebox

from pywriter.convert.yw7cnv import Yw7Cnv
from pywriter.core.yw7file import Yw7File


TITLE = 'PyWriter v1.2'


class CnvRunner(Yw7Cnv):

    def __init__(self, sourcePath, document, extension, silentMode=True):
        """File conversion for proofreading """
        root = Tk()
        root.geometry("640x480")
        root.title(TITLE)
        self.header = Label(root, text=__doc__)
        self.header.pack(padx=10, pady=10)
        self.label = Label(root, text='')
        self.label.pack(padx=10, pady=10)
        self.messagelabel = Label(root, text='')
        self.messagelabel.pack(padx=5, pady=5)

        self.silentMode = silentMode

        self.run(sourcePath, document, extension)

        if not silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.config(height=1, width=10)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def run(self, sourcePath, document, extension):
        """File conversion for proofreading """
        sourceFile = os.path.split(sourcePath)
        pathToSource = sourceFile[0]
        if pathToSource is not None:
            if pathToSource != '':
                pathToSource = pathToSource + '/'

        if sourceFile[1].endswith('.yw7'):
            yw7Path = pathToSource + sourceFile[1]
            document.filePath = pathToSource + \
                sourceFile[1].split('.yw7')[0] + '.' + extension
            self.label.config(
                text='Export yWriter7 scenes to .' + extension)
            self.messagelabel.config(text='Project: "' + yw7Path + '"')

            yw7File = Yw7File(yw7Path)

            self.messagelabel.config(
                text=self.yw7_to_document(yw7File, document))

        elif sourceFile[1].endswith('.' + extension):
            document.filePath = pathToSource + sourceFile[1]
            yw7Path = pathToSource + \
                sourceFile[1].split('.' + extension)[0] + '.yw7'
            self.label.config(
                text='Import yWriter7 scenes from .' + extension)
            self.messagelabel.config(
                text='Proofed scenes in "' + document.filePath + '"')

            yw7File = Yw7File(yw7Path)

            self.messagelabel.config(
                text=self.document_to_yw7(document, yw7File))

        else:
            self.messagelabel.config(
                text='Argument missing (drag and drop error?)\nInput file must be .yw7 or .' + extension + ' type.')

    def confirm_overwrite(self, file):
        """ Invoked by subclass if file already exists. """
        if self.silentMode:
            return(True)
        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' +
                                       file + '"?')
