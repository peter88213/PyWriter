"""Import and export ywriter7 scenes for proofing.

Proof reading with console user interface.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.proof.documentconverter import DocumentConverter


class ProofCnvRunner(DocumentConverter):

    def __init__(self, sourcePath, extension, silentMode=True):
        """ File conversion for proofreading """
        self.silentMode = silentMode
        sourceFile = os.path.split(sourcePath)
        pathToSource = sourceFile[0]
        if pathToSource:
            pathToSource = pathToSource + '/'

        if sourceFile[1].count('.yw7'):
            self.yw7Path = pathToSource + sourceFile[1]
            self.documentPath = pathToSource + \
                sourceFile[1].split('.yw7')[0] + '.' + extension
            print('\n*** Export yWriter7 scenes to .' + extension + ' ***')
            print('Project: "' + self.yw7Path + '"')
            DocumentConverter.__init__(self, self.yw7Path, self.documentPath)
            print(self.yw7_to_document())
            self.postprocess()

        elif sourceFile[1].count('.' + extension):
            self.documentPath = pathToSource + sourceFile[1]
            self.yw7Path = pathToSource + \
                sourceFile[1].split('.' + extension)[0] + '.yw7'
            print('\n*** Import yWriter7 scenes from .' + extension + ' ***')
            print('Proofed scenes in "' + self.documentPath + '"')
            DocumentConverter.__init__(self, self.yw7Path, self.documentPath)
            print(self.document_to_yw7())

        else:
            print('Input file must be .yw7 or .' + extension + ' type.')

        if not silentMode:
            input('Press ENTER to continue ...')

    def postprocess(self):
        pass

    def confirm_overwrite(self, file):
        if not self.silentMode:
            print('\nWARNING: This will overwrite "' +
                  file + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit(1)
