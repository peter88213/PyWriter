""" Python unit tests for the pyWriter project.

Test the "export project" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
from pywriter.html.html_to_yw7 import html_to_yw7
from pywriter.html.yw7_to_html import yw7_to_html

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

HTML_FILE = TEST_PROJECT + '.html'
HTML_EXPORTED_FILE = 'exported/' + TEST_PROJECT + '.html'

YW7_FILE = TEST_PROJECT + '.yw7'
YW7_EXPORTED_FILE = 'exported/' + TEST_PROJECT + '.yw7'


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
        os.remove(TEST_EXEC_PATH + HTML_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + YW7_FILE)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """ Test case: Normal operation

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
        """ Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW7_FILE),
            read_file(TEST_DATA_PATH + YW7_EXPORTED_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + HTML_FILE),
            read_file(TEST_DATA_PATH + HTML_EXPORTED_FILE))

    #@unittest.skip('development')
    def test_exp_to_html(self):
        """ Export yW7 scenes to html. """
        yw7_to_html(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + HTML_FILE)
        # Read .yw7 file and convert scenes to html.

        self.assertEqual(read_file(TEST_EXEC_PATH + HTML_FILE),
                         read_file(TEST_DATA_PATH + HTML_FILE))
        # Verify the html file.

    #@unittest.skip('development')
    def test_imp_from_html(self):
        """ Import proofed yw7 scenes from html . """
        copy_file(TEST_DATA_PATH + HTML_EXPORTED_FILE,
                  TEST_EXEC_PATH + HTML_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        html_to_yw7(TEST_EXEC_PATH + HTML_FILE,
                    TEST_EXEC_PATH + YW7_FILE)
        # Convert document to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_EXPORTED_FILE))
        # Verify the yw7 project.

    #@unittest.skip('development')
    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
