""" Import and export ywriter7 scenes for proofing.

    Proof reading file format = DOCX (Office Open XML format)

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
from pywriter.proof.yw7_to_md import yw7_to_md
from pywriter.proof.md_to_yw7 import md_to_yw7
from pywriter.proof.md_to_docx import md_to_docx
from pywriter.proof.docx_to_md import docx_to_md


def yw7_to_docx(yw7File, mdFile, docxFile):
    """ Export to docx """
    message = yw7_to_md(yw7File, mdFile)
    if message.count('ERROR'):
        return(message)
    try:
        os.remove(docxFile)
    except(FileNotFoundError):
        pass
    md_to_docx(mdFile, docxFile)
    if os.path.isfile(docxFile):
        return(message.replace(mdFile, docxFile))
    else:
        return('\nERROR: Could not create file!')


def docx_to_yw7(docxFile, mdFile, yw7File):
    """ Import from yw7 """
    docx_to_md(docxFile, mdFile)
    message = md_to_yw7(mdFile, yw7File)
    return(message)


try:
    sourcePath = sys.argv[1]

except:
    print('Syntax: proofdocx.py filename')
    exit(1)

if not os.path.isfile(sourcePath):
    print('\nERROR: File "' + sourcePath + '" not found.')
    exit(1)

sourceFile = os.path.split(sourcePath)
pathToSource = sourceFile[0]
if pathToSource:
    pathToSource = pathToSource + '/'
if sourceFile[1].count('.yw7'):
    yw7File = pathToSource + sourceFile[1]
    mdFile = pathToSource + sourceFile[1].split('.yw7')[0] + '.md'
    docxFile = pathToSource + \
        sourceFile[1].split('.yw7')[0] + '.docx'
    print('\n*** Export yWriter7 scenes to ODT ***')
    print('Project: "' + yw7File + '"')
    if os.path.isfile(docxFile):
        print('\nWARNING: This will overwrite "' +
              docxFile + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if not userConfirmation in ('y', 'Y'):
            print('Program abort by user.\n')
            input('Press ENTER to continue ...')
            sys.exit()
    print(yw7_to_docx(yw7File, mdFile, docxFile))

elif sourceFile[1].count('.docx'):
    docxFile = pathToSource + sourceFile[1]
    mdFile = pathToSource + sourceFile[1].split('.docx')[0] + '.md'
    yw7File = pathToSource + \
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
