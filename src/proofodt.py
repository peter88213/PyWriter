""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_odt(yw7File, mdFile, odtFile):
    """ Export to odt """
    message = pywriter.yw7_to_markdown(yw7File, mdFile)
    pywriter.markdown_to_odt(mdFile, odtFile)
    return(message)


def odt_to_yw7(odtFile, mdFile, yw7File):
    """ Import from odt """
    pywriter.odt_to_markdown(odtFile, mdFile)
    message = pywriter.markdown_to_yw7(mdFile, yw7File)
    return(message)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
    except:
        print('Syntax: proofodt.py filename')
        exit(1)

    sourceFile = os.path.split(sourcePath)
    if sourceFile[1].count('.yw7'):
        yw7File = sourceFile[0] + '/' + sourceFile[1]
        mdFile = sourceFile[0] + '/' + sourceFile[1].split('.yw7')[0] + '.md'
        odtFile = sourceFile[0] + '/' + \
            sourceFile[1].split('.yw7')[0] + '.odt'
        print('*** Export yWriter7 scenes to ODT ***')
        print('Project: "', yw7File, '"')
        print('\nWARNING: This will overwrite "' +
              odtFile + '" (if exists)!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(yw7_to_odt(yw7File, mdFile, odtFile))
        else:
            print('Program abort by user.\n')

    elif sourceFile[1].count('.odt'):
        odtFile = sourceFile[0] + '/' + sourceFile[1]
        mdFile = sourceFile[0] + '/' + sourceFile[1].split('.odt')[0] + '.md'
        yw7File = sourceFile[0] + '/' + \
            sourceFile[1].split('.odt')[0] + '.yw7'
        print('*** Import yWriter7 scenes from ODT ***')
        print('Proofed scenes in "', odtFile, '"')
        print('\nWARNING: This will overwrite "' +
              yw7File + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(odt_to_yw7(odtFile, mdFile, yw7File))
        else:
            print('Program abort by user.\n')
    else:
        print('Input file must be YW7 or ODT.')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
