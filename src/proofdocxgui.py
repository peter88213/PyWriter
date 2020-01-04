"""Import and export ywriter7 scenes for proofing.

Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os
from tkinter import *
from tkinter import messagebox

from pywriter.proof.documentconverter import DocumentConverter


class DCnvRunner(DocumentConverter):

    def __init__(self, sourcePath, extension):
        """File conversion for proofreading """
        self.extension = extension
        self.sourcePath = sourcePath

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
            label.config(
                text='Export yWriter7 scenes to .' + self.extension)
            messagelabel.config(text='Project: "' + self.yw7Path + '"')
            DocumentConverter.__init__(self, self.yw7Path, self.documentPath)
            messagelabel.config(text=self.yw7_to_document())

        elif sourceFile[1].count('.' + self.extension):
            self.documentPath = pathToSource + sourceFile[1]
            self.yw7Path = pathToSource + \
                sourceFile[1].split('.' + self.extension)[0] + '.yw7'
            label.config(
                text='Import yWriter7 scenes from .' + self.extension)
            messagelabel.config(
                text='Proofed scenes in "' + self.documentPath + '"')
            DocumentConverter.__init__(self, self.yw7Path, self.documentPath)
            messagelabel.config(text=self.document_to_yw7())

        else:
            messagelabel.config(
                text='Input file must be .yw7 or .' + self.extension + ' type.')

    def confirm_overwrite(self, file):
        """ Invoked by subclass if file already exists. """
        return messagebox.askyesno('WARNING', 'Overwrite existing file "' +
                                   file + '"?')


def run(sourcePath):
    myConverter = DCnvRunner(sourcePath, 'docx')
    myConverter.run()


if __name__ == '__main__':
    try:
        projectPath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    root = Tk()
    label = Label(root, text='yWriter proofer')
    label.pack(padx=10, pady=10)

    message = ''

    messagelabel = Label(root, text=message)
    messagelabel.pack(padx=5, pady=5)
    '''
    root.convertButton = Button(
        text='convert', command=lambda: run(projectPath))
    root.convertButton.pack(padx=5, pady=5)
    '''
    run(projectPath)
    root.quitButton = Button(text="OK", command=quit)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
