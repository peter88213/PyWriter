"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = ODT (OASIS Open Document format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.odtconverter import OdtConverter


class MyOdtConverter(OdtConverter):

    def __init__(self, yw7File, odtFile, silentMode=True):
        OdtConverter.__init__(self, yw7File, odtFile)
        self.silentMode = silentMode

    def confirm_overwrite(self, file):
        if not self.silentMode:
            print('\nWARNING: This will overwrite "' +
                  file + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit(1)


def run(sourcePath, silentMode=True):
    """ File conversion for proofreading """
    sourceFile = os.path.split(sourcePath)
    pathToSource = sourceFile[0]
    if pathToSource:
        pathToSource = pathToSource + '/'

    if sourceFile[1].count('.yw7'):
        yw7File = pathToSource + sourceFile[1]
        odtFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.odt'
        myConverter = MyOdtConverter(yw7File, odtFile, silentMode)
        print('\n*** Export yWriter7 scenes to .odt ***')
        print('Project: "' + yw7File + '"')
        print(myConverter.yw7_to_odt())

    elif sourceFile[1].count('.odt'):
        odtFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.odt')[0] + '.yw7'
        myConverter = MyOdtConverter(yw7File, odtFile, silentMode)
        print('\n*** Import yWriter7 scenes from .odt ***')
        print('Proofed scenes in "' + odtFile + '"')
        print(myConverter.odt_to_yw7())

    else:
        print('Input file must be .yw7 or .odt type.')

    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
