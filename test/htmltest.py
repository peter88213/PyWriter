"""Integration tests for the pyWriter project.

Test the "export project" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
from pywriter.proof.htmlconverter import HtmlConverter

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

HTML_FILE = TEST_PROJECT + '.html'
HTML_PROOFED_FILE = 'proof/' + TEST_PROJECT + '.html'

YW7_FILE = TEST_PROJECT + '.yw7'
YW7_PROOFED_FILE = 'proof/htmltest.yw7'

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
        os.remove(TEST_EXEC_PATH + HTML_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + YW7_FILE)
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
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + HTML_FILE),
            read_file(TEST_DATA_PATH + HTML_PROOFED_FILE))

    def test_yw7_to_html(self):
        """Export yW7 scenes to html. """

        converter = HtmlConverter(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + HTML_FILE)
        self.assertEqual(converter.yw7_to_html(
        ), 'SUCCESS: "' + TEST_EXEC_PATH + HTML_FILE + '" saved.')
        # Read .yw7 file and convert scenes to html.

        self.assertEqual(read_file(TEST_EXEC_PATH + HTML_FILE),
                         read_file(TEST_DATA_PATH + HTML_FILE))
        # Verify the html file.

    def test_html_to_yw7(self):
        """Import proofed yw7 scenes from html. """

        copy_file(TEST_DATA_PATH + HTML_PROOFED_FILE,
                  TEST_EXEC_PATH + HTML_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        converter = HtmlConverter(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + HTML_FILE)
        self.assertEqual(converter.html_to_yw7(
        ), 'SUCCESS: ' + str(TOTAL_SCENES) + ' Scenes written to "' + TEST_EXEC_PATH + YW7_FILE + '".')
        # Convert document to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
