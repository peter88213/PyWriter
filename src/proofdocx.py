""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_docx(yw7File, mdFile, docxFile):
    """ Export to docx """
    message = pywriter.yw7_to_markdown(yw7File, mdFile)
    pywriter.markdown_to_docx(mdFile, docxFile)
    return(message)


def docx_to_yw7(docxFile, mdFile, yw7File):
    """ Import from markdown """
    pywriter.docx_to_markdown(docxFile, mdFile)
    message = pywriter.markdown_to_yw7(mdFile, yw7File)
    return(message)


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
        docxFile = sourceFile[0] + '/' + \
            sourceFile[1].split('.yw7')[0] + '.docx'
        print('*** Export yWriter7 scenes to ODT ***')
        print('Project: "', yw7File, '"')
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
        print('*** Import yWriter7 scenes from DOCX ***')
        print('Proofed scenes in "', docxFile, '"')
        print('\nWARNING: This will overwrite "' +
              yw7File + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(docx_to_yw7(docxFile, mdFile, yw7File))
        else:
            print('Program abort by user.\n')
    else:
        print('Input file must be YW7 or DOCX.')
    input('Press ENTER to continue ...')


if __name__ == '__main__':
    main()
