""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_odt(yw7File, mdFile, odtFile):
    """ Export to odt """
    pywriter.yw7_to_markdown(yw7File, mdFile)
    pywriter.markdown_to_odt(mdFile, odtFile)


def odt_to_yw7(odtFile, mdFile, yw7File):
    """ Import from markdown """
    pywriter.odt_to_markdown(odtFile, mdFile)
    pywriter.markdown_to_yw7(mdFile, yw7File)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
    except:
        print('ERROR: "' + sourcePath + '" is no valid input!')
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
            yw7_to_odt(yw7File, mdFile, odtFile)
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
            odt_to_yw7(odtFile, mdFile, yw7File)
        else:
            print('Program abort by user.\n')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
