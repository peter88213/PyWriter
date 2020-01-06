"""Import and export ywriter7 scenes for proofing. 

Proof reading file format: html (with invisible chapter and scene tags).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from tkinter import *
from tkinter import messagebox

from pywriter.edit.manuscriptcnv import ManuscriptCnv


TITLE = 'PyWriter v1.1'


class MCnvRunner(ManuscriptCnv):

    def __init__(self, sourcePath, extension, silentMode=True):
        """File conversion for proofreading """
        self.silentMode = silentMode
        self.extension = extension
        self.sourcePath = sourcePath
        root = Tk()
        root.geometry("640x480")
        root.title(TITLE)
        self.header = Label(root, text=__doc__)
        self.header.pack(padx=10, pady=10)
        self.label = Label(root, text='')
        self.label.pack(padx=10, pady=10)
        self.messagelabel = Label(root, text='')
        self.messagelabel.pack(padx=5, pady=5)
        self.run()
        if not self.silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.config(height=1, width=10)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def run(self):
        """File conversion for proofreading """
        sourceFile = os.path.split(self.sourcePath)
        pathToSource = sourceFile[0]
        if pathToSource is not None:
            pathToSource = pathToSource + '/'

        if sourceFile[1].endswith('.yw7'):
            self.yw7Path = self.sourcePath
            self.documentPath = pathToSource + \
                sourceFile[1].split('.yw7')[0] + self.extension + '.html'
            self.label.config(
                text='Export yWriter7 scenes to manuscript')
            self.messagelabel.config(text='Project: "' + self.yw7Path + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            self.messagelabel.config(text=self.yw7_to_document())

        elif sourceFile[1].endswith(self.extension + '.html'):
            self.documentPath = self.sourcePath
            self.yw7Path = pathToSource + \
                sourceFile[1].split(self.extension)[0] + '.yw7'
            self.label.config(
                text='Import yWriter7 scenes from .' + self.extension)
            self.messagelabel.config(
                text='Proofed scenes in "' + self.documentPath + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            self.messagelabel.config(text=self.document_to_yw7())

        else:
            self.messagelabel.config(
                text='Argument missing (drag and drop error?)\nInput file must be .yw7 or manuscript.html type.')

    def confirm_overwrite(self, file):
        """ Invoked by subclass if file already exists. """
        if self.silentMode:
            return(True)
        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' +
                                       file + '"?')
