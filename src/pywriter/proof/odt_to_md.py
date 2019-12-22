""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.proof.pandoc import convert_file


def odt_to_md(odtFile, mdFile):
    """ Let pandoc read .odt file and convert to markdown. """
    convert_file(odtFile, 'markdown_strict', format='odt',
                 outputfile=mdFile, extra_args=['--wrap=none'])


if __name__ == '__main__':
    pass
