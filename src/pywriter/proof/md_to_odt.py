""" Library for yWriter 7 file operations

For further information see https://github.com/peter88213/Pyw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.proof.pandoc import convert_file


def md_to_odt(mdFile, odtFile):
    """ Let pandoc convert markdown and write to .odt file. """
    convert_file(mdFile, 'odt', format='markdown_strict', outputfile=odtFile)


if __name__ == '__main__':
    pass
