""" Create ODT for yWriter proofing.

A Pandoc wrapper for Python modules.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import pypandoc


def markdown_to_docx(mdFile, docxFile):
    """ Let pandoc convert markdown and write to .docx file. """
    pypandoc.convert_file(
        mdFile, 'docx', format='markdown_strict', outputfile=docxFile)


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: mddocx.py filename.md')
        sys.exit(1)

    docxPath = mdPath.split('.md')[0] + '.docx'
    markdown_to_docx(mdPath, docxPath)


if __name__ == '__main__':
    main()
