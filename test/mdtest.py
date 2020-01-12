"""Integration tests for the pyWriter project.

Test the "proof read" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.converter.yw7cnv import Yw7Cnv
from pywriter.model.yw7file import Yw7File

from pywriter.model.mdfile import MdFile


TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

DOCUMENT_FILE = TEST_PROJECT + '.md'
DOCUMENT_PROOFED_FILE = 'proof/' + TEST_PROJECT + '.md'

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


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the markdown 
            file's content matches the reference. 
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
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + DOCUMENT_PROOFED_FILE),
            read_file(TEST_DATA_PATH + DOCUMENT_FILE))

    def test_yw7_to_md(self):
        """Export yW7 scenes to markdown. """

        yw7File = Yw7File(TEST_EXEC_PATH + YW7_FILE)
        documentFile = MdFile(TEST_EXEC_PATH + DOCUMENT_FILE)
        converter = Yw7Cnv()

        # Read .yw7 file and convert xml to markdown.

        self.assertEqual(converter.yw7_to_document(
            yw7File, documentFile), 'SUCCESS: "' + TEST_EXEC_PATH + DOCUMENT_FILE + '" saved.')

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_FILE),
                         read_file(TEST_DATA_PATH + DOCUMENT_FILE))

    def test_md_to_yw7(self):
        """Import proofed yw7 scenes from markdown . """

        copy_file(TEST_DATA_PATH + DOCUMENT_PROOFED_FILE,
                  TEST_EXEC_PATH + DOCUMENT_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(TEST_EXEC_PATH + YW7_FILE)
        documentFile = MdFile(TEST_EXEC_PATH + DOCUMENT_FILE)
        converter = Yw7Cnv()

        # Convert markdown to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw7(documentFile, yw7File), 'SUCCESS: ' + str(
            TOTAL_SCENES) + ' Scenes written to "' + TEST_EXEC_PATH + YW7_FILE + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
