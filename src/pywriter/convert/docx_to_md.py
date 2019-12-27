""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.convert.pypandoc import convert_file


def docx_to_md(docxFile, mdFile):
    """ Let pandoc read .docx file and convert to markdown. """
    convert_file(docxFile, 'markdown_strict', format='docx',
                 outputfile=mdFile, extra_args=['--wrap=none'])


if __name__ == '__main__':
    pass