"""Integration tests for the pyWriter project.

Test the html import tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile

from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator

from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/_import/'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
REFERENCE_HTML = DATA_PATH + 'normal.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def remove_all_tempfiles():

    try:
        os.remove(TEST_HTML)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the html 
            file's content matches the reference. 
    """

    def setUp(self):

        try:
            os.mkdir(EXEC_PATH)

        except:
            pass

        remove_all_tempfiles()

    def test_wip(self):
        """Import proofed yw7 scenes from html . """

        copy_file(REFERENCE_HTML, TEST_HTML)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(TEST_YW7)
        yw7File.ywTreeBuilder = Yw7TreeCreator()
        yw7File.ywProjectMerger = YwProjectCreator()
        documentFile = HtmlImport(TEST_HTML)
        converter = YwCnv()

        # Convert html to xml and replace .yw7 file.

        self.assertEqual(converter.convert(
            documentFile, yw7File), 'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(REFERENCE_YW7))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
