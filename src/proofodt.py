""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_odt(yw7File, mdFile, odtFile):
    """ Export to odt """
    message = pywriter.yw7_to_md(yw7File, mdFile)
    if message.count('ERROR'):
        return(message)
    try:
        os.remove(odtFile)
    except(FileNotFoundError):
        pass
    pywriter.md_to_odt(mdFile, odtFile)
    if os.path.isfile(odtFile):
        return(message.replace(mdFile, odtFile))
    else:
        return('\nERROR: Could not create file!')


def odt_to_yw7(odtFile, mdFile, yw7File):
    """ Import from odt """
    pywriter.odt_to_md(odtFile, mdFile)
    message = pywriter.md_to_yw7(mdFile, yw7File)
    return(message)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
    except:
        print('Syntax: proofodt.py filename')
        exit(1)

    sourceFile = os.path.split(sourcePath)
    pathToSource = sourceFile[0]
    if pathToSource:
        pathToSource = pathToSource + '/'
    if sourceFile[1].count('.yw7'):
        yw7File = pathToSource + sourceFile[1]
        mdFile = pathToSource + sourceFile[1].split('.yw7')[0] + '.md'
        odtFile = pathToSource + \
            sourceFile[1].split('.yw7')[0] + '.odt'
        print('\n*** Export yWriter7 scenes to ODT ***')
        print('Project: "' + yw7File + '"')
        if os.path.isfile(odtFile):
            print('\nWARNING: This will overwrite "' +
                  odtFile + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if not userConfirmation in ('y', 'Y'):
                print('Program abort by user.\n')
                input('Press ENTER to continue ...')
                sys.exit()
        print(yw7_to_odt(yw7File, mdFile, odtFile))

    elif sourceFile[1].count('.odt'):
        odtFile = pathToSource + sourceFile[1]
        mdFile = pathToSource + sourceFile[1].split('.odt')[0] + '.md'
        yw7File = pathToSource + \
            sourceFile[1].split('.odt')[0] + '.yw7'
        print('\n*** Import yWriter7 scenes from ODT ***')
        print('Proofed scenes in "' + odtFile + '"')
        if os.path.isfile(yw7File):
            print('\nWARNING: This will overwrite "' +
                  yw7File + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if userConfirmation in ('y', 'Y'):
                print(odt_to_yw7(odtFile, mdFile, yw7File))
            else:
                print('Program abort by user.\n')
        else:
            print('\n"' + yw7File + '" not found.')
            print(
                'Please make sure that your proofed file is in the same directory as your yWriter7 project.')
            print('Program abort.')
    else:
        print('Input file must be YW7 or ODT.')
    try:
        os.remove(mdFile)
    except:
        pass
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
