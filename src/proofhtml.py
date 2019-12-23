"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = HTML

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.html.html_to_yw7 import html_to_yw7
from pywriter.html.yw7_to_html import yw7_to_html


def confirm_overwrite(file):
    if os.path.isfile(file):
        print('\nWARNING: This will overwrite "' +
              file + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if not userConfirmation in ('y', 'Y'):
            print('Program abort by user.\n')
            input('Press ENTER to continue ...')
            return(False)
    return(True)


def run(sourcePath, silentMode=False):
    if not os.path.isfile(sourcePath):
        print('\nERROR: File "' + sourcePath + '" not found.')
        exit(1)

    sourceFile = os.path.split(sourcePath)
    pathToSource = sourceFile[0]
    if pathToSource:
        pathToSource = pathToSource + '/'
    if sourceFile[1].count('.yw7'):
        yw7File = pathToSource + sourceFile[1]
        htmlFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.html'
        print('\n*** Export yw7 scenes to html ***')
        print('Project: "' + yw7File + '"')
        if not silentMode:
            if not confirm_overwrite(htmlFile):
                sys.exit(1)

        print(yw7_to_html(yw7File, htmlFile))

    elif sourceFile[1].count('.html'):
        htmlFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.html')[0] + '.yw7'
        print('\n*** Import yw7 scenes from html ***')
        print('Proofed scenes in "' + htmlFile + '"')
        if not silentMode:
            if not confirm_overwrite(yw7File):
                sys.exit(1)

        if os.path.isfile(yw7File):
            print(html_to_yw7(htmlFile, yw7File))
        else:
            print('\n"' + yw7File + '" not found.')
            print(
                'Please make sure that your proofed file is in the same directory as your yWriter7 project.')
            print('Program abort.')
    else:
        print('Input file must be YW7 or html.')
    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        print(__doc__)
        exit(1)

    run(sourcePath)
