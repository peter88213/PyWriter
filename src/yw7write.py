'''
Created on 12.12.2019

@author: Peter
'''
import sys
import pypandoc


def format_md(text):
    text = text.replace('\r', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    return(text)


def odt_to_markdown(odtPath):
    prjText = pypandoc.convert_file(
        odtPath, 'markdown_strict', format='odt', extra_args=['--wrap=none'])
    prjText = format_md(prjText)
    return(prjText)


def main():
    """ Collect command line arguments, call conversion and generate string. """
    try:
        odtPath = sys.argv[1]
        prjText = odt_to_markdown(odtPath)
    except:
        print('Syntax: yw7read.py filename')
        sys.exit(1)

    mdPath = odtPath.split('.odt')[0] + '.md'
    with open(mdPath, 'w') as f:
        f.write(prjText)

    yw7Path = odtPath.split('.odt')[0] + '.yw7'


if __name__ == '__main__':
    main()
