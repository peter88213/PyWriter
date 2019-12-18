""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
    except:
        print('Syntax: proofmd.py filename')
        exit(1)

    sourceFile = os.path.split(sourcePath)
    if sourceFile[1].count('.yw7'):
        yw7File = sourceFile[0] + '/' + sourceFile[1]
        mdFile = sourceFile[0] + '/' + \
            sourceFile[1].split('.yw7')[0] + '.md'
        print('\n*** Export yw7 scenes to Markdown (Strict) ***')
        print('Project: "', yw7File, '"')
        print('\nWARNING: This will overwrite "' +
              mdFile + '" (if exists)!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(pywriter.yw7_to_markdown(yw7File, mdFile))
        else:
            print('Program abort by user.\n')

    elif sourceFile[1].count('.md'):
        mdFile = sourceFile[0] + '/' + sourceFile[1]
        yw7File = sourceFile[0] + '/' + \
            sourceFile[1].split('.md')[0] + '.yw7'
        print('\n*** Import yw7 scenes from Markdown (Strict) ***')
        print('Proofed scenes in "', mdFile, '"')
        print('\nWARNING: This will overwrite "' +
              yw7File + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(pywriter.markdown_to_yw7(mdFile, yw7File))
        else:
            print('Program abort by user.\n')
    else:
        print('Input file must be YW7 or md.')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
