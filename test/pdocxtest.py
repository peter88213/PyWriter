""" Python unit tests for the yWrestler project.

Test the MS Word docx conversion.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import pywriter

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

DOCX_FILE = 'project.docx'
MD_FILE = 'project.md'
MD_REFERENCE_FILE = 'original.md'


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
            os.remove(TEST_EXEC_PATH + DOCX_FILE)
        except:
            pass
        copy_file(TEST_DATA_PATH + MD_REFERENCE_FILE,
                  TEST_EXEC_PATH + MD_FILE)

    def test_roundtrip(self):
        """ Convert md to docx and back to md. """
        pywriter.markdown_to_docx(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + DOCX_FILE)
        os.remove(TEST_EXEC_PATH + MD_FILE)
        pywriter.docx_to_markdown(TEST_EXEC_PATH + DOCX_FILE,
                                  TEST_EXEC_PATH + MD_FILE)
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))
        # Verify the yw7 project.


def main():
    unittest.main()


if __name__ == '__main__':
    main()
