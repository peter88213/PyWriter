"""Integration tests for the PyWriter distributions.

Test the .docx "proof read" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile

from pywriter.convert.yw7cnv import Yw7Cnv
from pywriter.core.yw7file import Yw7File

from pywriter.proof.officefile import OfficeFile

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = '../test'
TEST_EXEC_PATH = TEST_PATH + '/yw7/'
TEST_DATA_PATH = TEST_PATH + '/data/'

DOCUMENT_FILE = TEST_PROJECT + '.docx'
DOCUMENT_PROOFED_FILE = 'proof/' + TEST_PROJECT + '.docx'
DOCUMENT_CONTENT = 'word/document.xml'

YW7_FILE = TEST_PROJECT + '.yw7'
YW7_PROOFED_FILE = 'proof/' + TEST_PROJECT + '.yw7'

with open(TEST_DATA_PATH + YW7_FILE, 'r') as f:
    TOTAL_SCENES = f.read().count('<SCENE>')


def read_file(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def remove_all_testfiles():
    try:
        os.remove(TEST_EXEC_PATH + DOCUMENT_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + YW7_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCUMENT_CONTENT)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the intermediate
                    markdown file content matches 
                    the corresponding reference string. 
    """

    def setUp(self):
        remove_all_testfiles()
        copy_file(TEST_DATA_PATH + YW7_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_data(self):
        """Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW7_FILE),
            read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def test_yw7_to_docx(self):
        """Convert markdown to docx. """

        copy_file(TEST_DATA_PATH + YW7_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

        yw7File = Yw7File(TEST_EXEC_PATH + YW7_FILE)
        documentFile = OfficeFile(TEST_EXEC_PATH + DOCUMENT_FILE)
        converter = Yw7Cnv()

        self.assertEqual(converter.yw7_to_document(
            yw7File, documentFile), 'SUCCESS: "' + TEST_EXEC_PATH + DOCUMENT_FILE + '" saved.')

        with zipfile.ZipFile(TEST_EXEC_PATH + DOCUMENT_FILE, 'r') as myzip:
            myzip.extract(DOCUMENT_CONTENT, TEST_EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_CONTENT),
                         read_file(TEST_DATA_PATH + DOCUMENT_CONTENT))

    def test_docx_to_yw7(self):
        """Convert docx to markdown. """

        copy_file(TEST_DATA_PATH + DOCUMENT_PROOFED_FILE,
                  TEST_EXEC_PATH + DOCUMENT_FILE)

        yw7File = Yw7File(TEST_EXEC_PATH + YW7_FILE)
        documentFile = OfficeFile(TEST_EXEC_PATH + DOCUMENT_FILE)
        converter = Yw7Cnv()

        self.assertEqual(converter.document_to_yw7(documentFile, yw7File), 'SUCCESS: ' + str(
            TOTAL_SCENES) + ' Scenes written to "' + TEST_EXEC_PATH + YW7_FILE + '".')

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
