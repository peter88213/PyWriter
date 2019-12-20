""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


try:
    sourcePath = sys.argv[1]
except:
    print('Syntax: proofhtml.py filename')
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
    if os.path.isfile(htmlFile):
        print('\nWARNING: This will overwrite "' +
              htmlFile + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if not userConfirmation in ('y', 'Y'):
            print('Program abort by user.\n')
            input('Press ENTER to continue ...')
            sys.exit()
    print(pywriter.yw7_to_html(yw7File, htmlFile))

elif sourceFile[1].count('.html'):
    htmlFile = pathToSource + sourceFile[1]
    yw7File = pathToSource + \
        sourceFile[1].split('.html')[0] + '.yw7'
    print('\n*** Import yw7 scenes from html ***')
    print('Proofed scenes in "' + htmlFile + '"')
    if os.path.isfile(yw7File):
        print('\nWARNING: This will overwrite "' +
              yw7File + '"!')
        userConfirmation = input('Continue (y/n)? ')
        if userConfirmation in ('y', 'Y'):
            print(pywriter.html_to_yw7(htmlFile, yw7File))
        else:
            print('Program abort by user.\n')
    else:
        print('\n"' + yw7File + '" not found.')
        print(
            'Please make sure that your proofed file is in the same directory as your yWriter7 project.')
        print('Program abort.')
else:
    print('Input file must be YW7 or html.')
input('Press ENTER to continue ...')
