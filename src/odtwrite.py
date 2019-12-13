""" Create ODT for yWriter proofing.

    A Pandoc wrapper for Python modules.
"""
import sys
import pypandoc


def read_md(mdFile):
    """ Read markdown from .md file. """
    with open(mdFile, 'r') as f:
        mdText = f.read()
    return(mdText)


def markdown_to_odt(prjText, odtFile):
    """ Let pandoc convert markdown and write to .odt file. """
    pypandoc.convert_text(
        prjText, 'odt', format='markdown_strict', outputfile=odtFile)


def main():
    """ Call the functions with command line arguments. """
    try:
        mdPath = sys.argv[1]
    except:
        print('Syntax: odtwrite.py filename.md')
        sys.exit(1)

    prjText = read_md(mdPath)
    # Read markdown from .md file.
    odtPath = mdPath.split('.md')[0] + '.odt'
    markdown_to_odt(prjText, odtPath)
    # Let pandoc convert markdown and write to .odt file.


if __name__ == '__main__':
    main()
