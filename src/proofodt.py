""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_odt(sourceFile):
    """ Export to odt """
    mdFile = sourceFile[0] + sourceFile[1].split('.yw7')[0] + '.md'
    pywriter.yw7_to_markdown(sourceFile[0] + sourceFile[1], mdFile)
    odtFile = sourceFile[0] + sourceFile[1].split('.yw7')[0] + '.odt'
    pywriter.markdown_to_odt(mdFile, odtFile)


def odt_to_yw7(sourceFile):
    """ Import from markdown """
    mdFile = sourceFile[0] + sourceFile[1].split('.odt')[0] + '.md'
    pywriter.odt_to_markdown(sourceFile[0] + sourceFile[1], mdFile)
    yw7File = sourceFile[0] + sourceFile[1].split('.odt')[0] + '.yw7'
    pywriter.markdown_to_yw7(mdFile, yw7File)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
        sourceFile = os.path.split(sourcePath)
        if sourceFile[1].count('.yw7'):
            yw7_to_odt(sourceFile)
        elif sourceFile[1].count('.odt'):
            odt_to_yw7(sourceFile)
        x = input('Press any key ...')
    except:
        pass


if __name__ == '__main__':
    main()
