""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_docx(yw7File, mdFile, docxFile):
    """ Export to docx """
    message = pywriter.yw7_to_md(yw7File, mdFile)
    if message.count('ERROR'):
        return(message)
    try:
        os.remove(docxFile)
    except(FileNotFoundError):
        pass
    pywriter.md_to_docx(mdFile, docxFile)
    if os.path.isfile(docxFile):
        return(message.replace(mdFile, docxFile))
    else:
        return('\nERROR: Could not create file!')


def docx_to_yw7(docxFile, mdFile, yw7File):
    """ Import from yw7 """
    pywriter.docx_to_md(docxFile, mdFile)
    message = pywriter.md_to_yw7(mdFile, yw7File)
    return(message)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
    except:
        print('Syntax: proofdocx.py filename')
        exit(1)

    sourceFile = os.path.split(sourcePath)
    if sourceFile[1].count('.yw7'):
        yw7File = sourceFile[0] + '/' + sourceFile[1]
        mdFile = sourceFile[0] + '/' + sourceFile[1].split('.yw7')[0] + '.md'
        docxFile = sourceFile[0] + '/' + \
            sourceFile[1].split('.yw7')[0] + '.docx'
        print('\n*** Export yWriter7 scenes to ODT ***')
        print('Project: "' + yw7File + '"\n')
        print('\nWARNING: This will overwrite "' +
              docxFile + '" (if exists)!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(yw7_to_docx(yw7File, mdFile, docxFile))
        else:
            print('Program abort by user.\n')

    elif sourceFile[1].count('.docx'):
        docxFile = sourceFile[0] + '/' + sourceFile[1]
        mdFile = sourceFile[0] + '/' + sourceFile[1].split('.docx')[0] + '.md'
        yw7File = sourceFile[0] + '/' + \
            sourceFile[1].split('.docx')[0] + '.yw7'
        print('\n*** Import yWriter7 scenes from DOCX ***')
        print('Proofed scenes in "' + docxFile + '"')
        if os.path.isfile(yw7File):
            print('\nWARNING: This will overwrite "' +
                  yw7File + '"!')
            userConfirmation = input('Continue (y/n)? ')
            if userConfirmation in ('y', 'Y'):
                print(docx_to_yw7(docxFile, mdFile, yw7File))
            else:
                print('Program abort by user.\n')
        else:
            print('\n"' + yw7File + '" not found.')
            print(
                'Please make sure that your proofed file is in the same directory as your yWriter7 project.')
            print('Program abort.')
    else:
        print('Input file must be YW7 or DOCX.')
    try:
        os.remove(mdFile)
    except:
        pass
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
