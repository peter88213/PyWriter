"""Integration tests for the PyWriter distributions.

Test the .docx "proof read" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile
from pywriter.proof.documentconverter import DocumentConverter

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = '../test'
TEST_EXEC_PATH = TEST_PATH + '/yw7/'
TEST_DATA_PATH = TEST_PATH + '/data/'

DOCX_FILE = TEST_PROJECT + '.docx'
DOCX_PROOFED_FILE = 'proof/' + TEST_PROJECT + '.docx'
DOCX_CONTENT = 'word/document.xml'

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
        os.remove(TEST_EXEC_PATH + DOCX_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + YW7_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCX_CONTENT)
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
        myDocxConverter = DocumentConverter(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + DOCX_FILE)
        self.assertEqual(myDocxConverter.yw7_to_document(
        ), 'SUCCESS: "' + TEST_EXEC_PATH + DOCX_FILE + '" saved.')

        with zipfile.ZipFile(TEST_EXEC_PATH + DOCX_FILE, 'r') as myzip:
            myzip.extract(DOCX_CONTENT, TEST_EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCX_CONTENT),
                         read_file(TEST_DATA_PATH + DOCX_CONTENT))

    def test_docx_to_yw7(self):
        """Convert docx to markdown. """

        copy_file(TEST_DATA_PATH + DOCX_PROOFED_FILE,
                  TEST_EXEC_PATH + DOCX_FILE)
        myDocxConverter = DocumentConverter(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + DOCX_FILE)
        self.assertEqual(myDocxConverter.document_to_yw7(
        ), 'SUCCESS: ' + str(TOTAL_SCENES) + ' Scenes written to "' + TEST_EXEC_PATH + YW7_FILE + '".')

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
