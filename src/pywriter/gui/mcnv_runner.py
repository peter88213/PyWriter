"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from tkinter import *
from tkinter import messagebox

from pywriter.edit.manuscriptcnv import ManuscriptCnv


class MCnvRunner(ManuscriptCnv):

    def __init__(self, sourcePath, extension, silentMode=True):
        """File conversion for proofreading """
        self.silentMode = silentMode
        self.extension = extension
        self.sourcePath = sourcePath
        root = Tk()
        self.label = Label(root, text='yWriter proofer')
        self.label.pack(padx=10, pady=10)

        message = ''

        self.messagelabel = Label(root, text=message)
        self.messagelabel.pack(padx=5, pady=5)
        self.run()
        if not self.silentMode:
            root.quitButton = Button(text="OK", command=quit)
            root.quitButton.pack(padx=5, pady=5)
            root.mainloop()

    def run(self):
        """File conversion for proofreading """
        sourceFile = os.path.split(self.sourcePath)
        pathToSource = sourceFile[0]
        if pathToSource:
            pathToSource = pathToSource + '/'

        if sourceFile[1].count('.yw7'):
            self.yw7Path = pathToSource + sourceFile[1]
            self.documentPath = pathToSource + \
                sourceFile[1].split('.yw7')[0] + '.' + self.extension
            self.label.config(
                text='Export yWriter7 scenes to .' + self.extension)
            self.messagelabel.config(text='Project: "' + self.yw7Path + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            self.messagelabel.config(text=self.yw7_to_document())

        elif sourceFile[1].count('.' + self.extension):
            self.documentPath = pathToSource + sourceFile[1]
            self.yw7Path = pathToSource + \
                sourceFile[1].split('.' + self.extension)[0] + '.yw7'
            self.label.config(
                text='Import yWriter7 scenes from .' + self.extension)
            self.messagelabel.config(
                text='Proofed scenes in "' + self.documentPath + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            self.messagelabel.config(text=self.document_to_yw7())

        else:
            self.messagelabel.config(
                text='Input file must be .yw7 or .' + self.extension + ' type.')

    def confirm_overwrite(self, file):
        """ Invoked by subclass if file already exists. """
        if self.silentMode:
            return(True)
        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' +
                                       file + '"?')
