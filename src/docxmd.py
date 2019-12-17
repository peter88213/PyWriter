""" Convert proofed chapters to markdown. 

A Pandoc wrapper for Python modules.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import pypandoc


def docx_to_markdown(docxFile, mdFile):
    """ Let pandoc read .docx file and convert to markdown. """
    text = pypandoc.convert_file(
        docxFile, 'markdown_strict', format='docx', outputfile=mdFile, extra_args=['--wrap=none'])

    with open(mdFile, 'r', encoding='utf-8') as f:
        """ Beautify pandoc-generated md. """
        text = f.read()
        text = text.replace('\r', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\n', '\n\n')

    with open(mdFile, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    """ Call the functions with command line arguments. """
    try:
        docxPath = sys.argv[1]
    except:
        print('Syntax:docxmdd filenamedocx')
        sys.exit(1)

    mdPath = docxPath.split('docx')[0] + '.md'
    docx_to_markdown(docxPath, mdPath)


if __name__ == '__main__':
    main()
