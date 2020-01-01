"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = html with invisible chapter and scene tags

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.edit.contentconverter import ContentConverter


class CntCnvRunner(ContentConverter):

    def __init__(self, yw7Path, htmlPath, silentMode=True):
        ContentConverter.__init__(self, yw7Path, htmlPath)
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

        htmlFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.html'
        myConverter = CntCnvRunner(yw7File, htmlFile, silentMode)
        print('\n*** Export yWriter7 scenes to HTML ***')
        print('Project: "' + yw7File + '"')
        print(myConverter.yw7_to_html())

    elif sourceFile[1].count('.html'):
        htmlFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.html')[0] + '.yw7'
        myConverter = CntCnvRunner(yw7File, htmlFile, silentMode)
        print('\n*** Import yWriter7 scenes from HTML ***')
        print('Proofed scenes in "' + htmlFile + '"')
        print(myConverter.html_to_yw7())

    else:
        print('Input file must be .yw7 or .html type.')

    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        sys.exit(1)

    run(sourcePath, False)
