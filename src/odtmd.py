""" Convert proofed chapters to markdown. 

A Pandoc wrapper for Python modules.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import pypandoc


def format_md(text):
    """ Beautify pandoc-generated md. """
    text = text.replace('\r', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n\n', '\n')
    text = text.replace('\n', '\n\n')
    return(text)


def odt_to_markdown(odtFile, mdFile):
    """ Let pandoc read .odt file and convert to markdown. """
    text = pypandoc.convert_file(
        odtFile, 'markdown_strict', format='odt', extra_args=['--wrap=none'])
    text = format_md(text)
    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    """ Call the functions with command line arguments. """
    try:
        odtPath = sys.argv[1]
    except:
        print('Syntax: odtread.py filename.odt')
        sys.exit(1)

    mdPath = odtPath.split('.odt')[0] + '.md'
    odt_to_markdown(odtPath, mdPath)


if __name__ == '__main__':
    main()
