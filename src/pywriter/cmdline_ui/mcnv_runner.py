"""Import and export ywriter7 scenes for proofing.

Proof reading with console user interface.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os
from pywriter.edit.manuscriptcnv import ManuscriptCnv


class MCnvRunner(ManuscriptCnv):

    def __init__(self, sourcePath, extension, silentMode=True):
        """File conversion for proofreading """

        self.silentMode = silentMode
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
            print('\n*** Export yWriter7 scenes to .' + self.extension + ' ***')
            print('Project: "' + self.yw7Path + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            print(self.yw7_to_document())

        elif sourceFile[1].count('.' + self.extension):
            self.documentPath = pathToSource + sourceFile[1]
            self.yw7Path = pathToSource + \
                sourceFile[1].split('.' + self.extension)[0] + '.yw7'
            print('\n*** Import yWriter7 scenes from .' + self.extension + ' ***')
            print('Proofed scenes in "' + self.documentPath + '"')
            ManuscriptCnv.__init__(self, self.yw7Path, self.documentPath)
            print(self.document_to_yw7())

        else:
            print('Input file must be .yw7 or .' + self.extension + ' type.')

        if not self.silentMode:
            input('Press ENTER to continue ...')

    def confirm_overwrite(self, file):
        if not self.silentMode:
            print('\nWARNING: This will overwrite "' +
                  file + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit(1)
