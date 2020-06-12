"""Integration tests for the pyWriter project.

Test the html conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile

from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw_new_file import YwNewFile

from pywriter.html.html_import import HtmlImport


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/_import/'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
WIP_HTML = DATA_PATH + 'normal.html'
OUTLINE_HTML = DATA_PATH + 'outline.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
WIP_YW7 = DATA_PATH + 'normal.yw7'
OUTLINE_YW7 = DATA_PATH + 'outline.yw7'


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


def remove_all_testfiles():

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
        remove_all_testfiles()

    def test_wip(self):
        """Import proofed yw7 scenes from html . """

        copy_file(WIP_HTML, TEST_HTML)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = YwNewFile(TEST_YW7)
        documentFile = HtmlImport(TEST_HTML)
        converter = YwCnv()

        # Convert html to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw(
            documentFile, yw7File), 'SUCCESS: project data written to "' + TEST_YW7 + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(WIP_YW7))

    @unittest.skip('')
    def test_outline(self):
        """Import proofed yw7 scenes from html . """

        copy_file(OUTLINE_HTML, TEST_HTML)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = YwNewFile(TEST_YW7)
        documentFile = HtmlImport(TEST_HTML)
        converter = YwCnv()

        # Convert html to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw(
            documentFile, yw7File), 'SUCCESS: project data written to "' + TEST_YW7 + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(OUTLINE_YW7))

    def tearDown(self):
        return
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
