"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with invisible chapter and scene tags

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.edit.manuscriptcnv import ManuscriptCnv


class EditManuscript(ManuscriptCnv):

    def __init__(self, sourcePath, silentMode=True):
        self.silentMode = silentMode

    def run(self):
        """ File conversion for proofreading """
        sourceFile = os.path.split(sourcePath)
        pathToSource = sourceFile[0]
        if pathToSource:
            pathToSource = pathToSource + '/'

        if sourceFile[1].count('.yw7'):
            yw7Path = pathToSource + sourceFile[1]

            htmlPath = pathToSource + \
                sourceFile[1].split('.yw7')[0] + '.manuscript'
            ManuscriptCnv.__init__(self, yw7Path, htmlPath)
            print('\n*** Export yWriter7 scenes for Editing ***')
            print('Project: "' + yw7Path + '"')
            print(myConverter.yw7_to_html())

        elif sourceFile[1].count('.manuscript'):
            htmlPath = pathToSource + sourceFile[1]
            yw7Path = pathToSource + \
                sourceFile[1].split('.manuscript')[0] + '.yw7'
            ManuscriptCnv.__init__(self, yw7Path, htmlPath)
            print('\n*** Import yWriter7 scenes from HTML ***')
            print('Edited scenes in "' + htmlPath + '"')
            print(myConverter.html_to_yw7())

        else:
            print('Input file must be .yw7 or .manuscript type.')

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


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    myConverter = EditManuscript(sourcePath, False)
    myConverter.run()
