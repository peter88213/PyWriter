""" Import and export ywriter7 scenes for proofing. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import pywriter


def yw7_to_docx(sourceFile):
    """ Export to docx """
    mdFile = sourceFile[0] + sourceFile[1].split('.yw7')[0] + '.md'
    pywriter.yw7_to_markdown(sourceFile[0] + sourceFile[1], mdFile)
    docxFile = sourceFile[0] + sourceFile[1].split('.yw7')[0] + '.docx'
    pywriter.markdown_to_docx(mdFile, docxFile)


def docx_to_yw7(sourceFile):
    """ Import from markdown """
    mdFile = sourceFile[0] + sourceFile[1].split('.docx')[0] + '.md'
    pywriter.docx_to_markdown(sourceFile[0] + sourceFile[1], mdFile)
    yw7File = sourceFile[0] + sourceFile[1].split('.docx')[0] + '.yw7'
    pywriter.markdown_to_yw7(mdFile, yw7File)


def main():
    """ Call the functions with command line arguments. """
    try:
        sourcePath = sys.argv[1]
        sourceFile = os.path.split(sourcePath)
        if sourceFile[1].count('.yw7'):
            yw7_to_docx(sourceFile)
        elif sourceFile[1].count('.docx'):
            docx_to_yw7(sourceFile)
    except:
        pass


if __name__ == '__main__':
    main()
