""" Python unit tests for the yWrestler project.

Test the proofreading roundtrip using markdown as intermediate format.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import pywriter

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

YW7_FILE = 'project.yw7'
MD_FILE = 'project.md'
YW7_REFERENCE_FILE = 'original.yw7'
MD_REFERENCE_FILE = 'original.md'
YW7_PROOFED_FILE = 'proofed.yw7'
MD_PROOFED_FILE = 'proofed.md'


def read_file(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the intermediate
                    markdown file content matches 
                    the corresponding reference string. 
    """

    def setUp(self):
        try:
            os.remove(TEST_EXEC_PATH + MD_FILE)
        except:
            pass
        # Place the correct yw7 project file.
        copy_file(TEST_DATA_PATH + YW7_REFERENCE_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_data(self):
        """ Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + MD_PROOFED_FILE),
            read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW7_REFERENCE_FILE),
            read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def test_export(self):
        """ Convert yw7 scenes to odt for proofing. """
        pywriter.yw7_to_markdown(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + MD_FILE)
        # Read .yw7 file and convert xml to markdown.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))

    def test_import(self):
        """ Read and replace proofed scenes. """
        copy_file(TEST_DATA_PATH + MD_PROOFED_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        pywriter.markdown_to_yw7(TEST_EXEC_PATH + MD_FILE,
                                 TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.


def main():
    unittest.main()


if __name__ == '__main__':
    main()
