""" Import proofed chapters. 
"""
import sys
import xml.etree.ElementTree as ET
import pypandoc


def format_md(text):
    """ Beautify pandoc-generated md """
    text = text.replace('\r', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    return(text)


def odt_to_markdown(odtFile):
    """ run pandoc to create a markdown string """
    prjText = pypandoc.convert_file(
        odtFile, 'markdown_strict', format='odt', extra_args=['--wrap=none'])
    prjText = format_md(prjText)
    return(prjText)


def write_markdown(prjText, mdFile):
    with open(mdFile, 'w') as f:
        f.write(prjText)


def markdown_to_yw7(prjText, yw7File):
    tree = ET.parse(yw7File)
    root = tree.getroot()  # all item attributes
    return()


def main():
    """ Collect command line arguments, call conversion and generate string. """
    try:
        odtPath = sys.argv[1]
        prjText = odt_to_markdown(odtPath)
    except:
        print('Syntax: yw7write.py filename')
        sys.exit(1)

    mdPath = odtPath.split('.odt')[0] + '.md'
    write_markdown(prjText, mdPath)

    yw7Path = odtPath.split('.odt')[0] + '.yw7'
    markdown_to_yw7(prjText, yw7Path)


if __name__ == '__main__':
    main()
