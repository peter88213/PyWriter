"""Integration tests for the pyWriter project.

Test the html conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile

from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw_file import YwFile

from pywriter.html.html_chapterdesc import HtmlChapterDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.globals import PARTDESC_SUFFIX


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/' + PARTDESC_SUFFIX + '/'

TEST_ODT = EXEC_PATH + 'yw7 Sample Project' + PARTDESC_SUFFIX + '.odt'
ODT_CONTENT = 'content.xml'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
REFERENCE_HTML = DATA_PATH + 'normal.html'
PROOFED_HTML = DATA_PATH + 'proofed.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'
PROOFED_YW7 = DATA_PATH + 'proofed.yw7'

TOTAL_SCENES = 56


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
        os.remove(TEST_ODT)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass
    try:
        os.remove(EXEC_PATH + ODT_CONTENT)
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
        copy_file(REFERENCE_YW7, TEST_YW7)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.

        self.assertNotEqual(
            read_file(REFERENCE_YW7),
            read_file(PROOFED_YW7))

    def test_html_to_yw7(self):
        """Import proofed yw7 scenes from html . """

        copy_file(PROOFED_HTML, TEST_HTML)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = YwFile(TEST_YW7)
        documentFile = HtmlChapterDesc(TEST_HTML)
        converter = YwCnv()

        # Convert html to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw(
            documentFile, yw7File), 'SUCCESS: project data written to "' + TEST_YW7 + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def test_yw7_to_odt(self):
        """Convert markdown to odt. """
        yw7File = YwFile(TEST_YW7)
        documentFile = OdtPartDesc(TEST_ODT)
        converter = YwCnv()

        self.assertEqual(converter.yw_to_document(
            yw7File, documentFile), 'SUCCESS: "' + TEST_ODT + '" saved.')

        with zipfile.ZipFile(TEST_ODT, 'r') as myzip:
            myzip.extract(ODT_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODT_CONTENT),
                         read_file(DATA_PATH + ODT_CONTENT))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
