""" Python unit tests for the yWrestler project.

Test the proofreading roundtrip using html as intermediate format.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import yw7html
import htmlyw7

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yWriter7 Sample/'
TEST_DATA_PATH = 'data/'

YW7_FILE = 'yW7 Sample Project.yw7'
HTML_FILE = 'yW7 Sample Project.html'
YW7_PROOFED_FILE = 'after_proofing.yw7'
HTML_PROOFED_FILE = 'after_proofing.html'


def read_file(inputFile):
    with open(inputFile, 'r') as f:
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
            os.remove(TEST_EXEC_PATH + HTML_FILE)
        except:
            pass
        # Place the correct yw7 project file.
        copy_file(TEST_DATA_PATH + YW7_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_data(self):
        """ Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + HTML_FILE),
            read_file(TEST_DATA_PATH + HTML_PROOFED_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW7_FILE),
            read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))

    def test_export(self):
        """ Convert yw7 scenes to html for proofing. """
        yw7html.yw7_to_html(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + HTML_FILE)
        # Read .yw7 file and convert scenes to html.
        self.assertEqual(read_file(TEST_EXEC_PATH + HTML_FILE),
                         read_file(TEST_DATA_PATH + HTML_FILE))
        # Verify the html file.

    def test_import(self):
        """ Read and replace proofed scenes. """
        copy_file(TEST_DATA_PATH + HTML_PROOFED_FILE,
                  TEST_EXEC_PATH + HTML_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.
        htmlyw7.html_to_yw7(TEST_EXEC_PATH + HTML_FILE,
                            TEST_EXEC_PATH + YW7_FILE)
        # Convert document to xml and replace .yw7 file.
        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the html file.


def main():
    unittest.main()


if __name__ == '__main__':
    main()
