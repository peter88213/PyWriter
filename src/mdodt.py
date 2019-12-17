""" Create ODT for yWriter proofing.

A Pandoc wrapper for Python modules.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import pypandoc


def markdown_to_odt(mdFile, odtFile):
    """ Let pandoc convert markdown and write to .odt file. """
    pypandoc.convert_file(
        mdFile, 'odt', format='markdown_strict', outputfile=odtFile)


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: odtwrite.py filename.md')
        sys.exit(1)

    odtPath = mdPath.split('.md')[0] + '.odt'
    markdown_to_odt(mdPath, odtPath)


if __name__ == '__main__':
    main()
