"""Import and export ywriter7 scenes for proofing. 

Proof reading file format = Markdown (strict) 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.proof.yw7_to_md import yw7_to_md
from pywriter.proof.md_to_yw7 import md_to_yw7


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
        mdFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.md'
        print('\n*** Export yw7 scenes to Markdown (Strict) ***')
        print('Project: "' + yw7File + '"')
        if not silentMode:
            if not confirm_overwrite(mdFile):
                sys.exit(1)

        print(yw7_to_md(yw7File, mdFile))

    elif sourceFile[1].count('.md'):
        mdFile = pathToSource + sourceFile[1]
        yw7File = pathToSource + \
            sourceFile[1].split('.md')[0] + '.yw7'
        print('\n*** Import yw7 scenes from Markdown (Strict) ***')
        print('Proofed scenes in "' + mdFile + '"')
        if not silentMode:
            if not confirm_overwrite(yw7File):
                sys.exit(1)

        if os.path.isfile(yw7File):
            print(md_to_yw7(mdFile, yw7File))
        else:
            print('\n"' + yw7File + '" not found.')
            print(
                'Please make sure that your proofed file is in the same directory as your yWriter7 project.')
            print('Program abort.')
    else:
        print('Input file must be YW7 or md.')
    if not silentMode:
        input('Press ENTER to continue ...')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]

    except:
        print(__doc__)
        exit(1)

    run(sourcePath, True)
