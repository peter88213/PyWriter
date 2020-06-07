"""Unit tests for the pyWriter project.

Test the html conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
from pywriter.html.html_form import *

TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/_import/'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
INPUT_HTML = DATA_PATH + 'normal.html'
REFERENCE_HTML = DATA_PATH + 'converted.html'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


class Parser(unittest.TestCase):

    def test_define_sections(self):
        text = read_html_file(INPUT_HTML)[1]
        text = define_sections(text)

        with open(TEST_HTML, 'w') as f:
            f.write(text)

        reference = read_file(REFERENCE_HTML)
        self.assertEqual(text, reference)
