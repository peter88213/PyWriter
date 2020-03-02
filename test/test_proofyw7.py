""" Python unit tests for the yW2OO project.

Test suite for proofyw7.py.

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import zipfile

import proofyw7


# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd()
TEST_DATA_PATH = 'data/odtproof/'
TEST_EXEC_PATH = 'yw7/'

# To be placed in TEST_DATA_PATH:

# Test data
YW7_TEST = TEST_EXEC_PATH + 'yWriter Sample Project.yw7'
ODT_TEST = TEST_EXEC_PATH + 'yWriter Sample Project_proof.odt'
HTML_TEST = TEST_EXEC_PATH + 'yWriter Sample Project_proof.html'

DOCUMENT_CONTENT = 'content.xml'
DOCUMENT_STYLES = 'styles.xml'

YW7_NORMAL = TEST_DATA_PATH + 'normal.yw7'
YW7_PROOFED = TEST_DATA_PATH + 'proofed.yw7'

DOC_NORMAL = TEST_DATA_PATH + 'normal.odt'
DOC_PROOFED = TEST_DATA_PATH + 'proofed.html'

with open(YW7_NORMAL, 'r') as f:
    TOTAL_SCENES = f.read().count('<SCENE>')


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
        os.remove(YW7_TEST)
    except:
        pass
    try:
        os.remove(ODT_TEST)
    except:
        pass
    try:
        os.remove(HTML_TEST)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCUMENT_STYLES)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCUMENT_CONTENT)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):
        copy_file(YW7_NORMAL, YW7_TEST)
        copy_file(DOC_PROOFED, HTML_TEST)
        try:
            os.remove(ODT_TEST)
        except:
            pass

    def test_data(self):
        """Verify test data integrity. """
        self.assertNotEqual(
            read_file(YW7_NORMAL),
            read_file(YW7_PROOFED))

    def test_yw7_to_odt(self):
        self.assertEqual(proofyw7.run(YW7_TEST),
                         'SUCCESS: "' + ODT_TEST + '" saved.')

        with zipfile.ZipFile(ODT_TEST, 'r') as myzip:
            myzip.extract(DOCUMENT_CONTENT, TEST_EXEC_PATH)
            myzip.extract(DOCUMENT_STYLES, TEST_EXEC_PATH)

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_CONTENT),
                         read_file(TEST_DATA_PATH + DOCUMENT_CONTENT))
        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_STYLES),
                         read_file(TEST_DATA_PATH + DOCUMENT_STYLES))

    def test_html_to_yw7(self):
        self.assertEqual(proofyw7.run(HTML_TEST),
                         'SUCCESS: ' + str(TOTAL_SCENES) + ' Scenes written to "' + YW7_TEST + '".')

        self.assertEqual(read_file(YW7_TEST), read_file(YW7_PROOFED))

    def tearDown(self):
        remove_all_testfiles()


class NoProjectFile(unittest.TestCase):
    """Test case: yWriter project file is not present."""

    def setUp(self):
        copy_file(DOC_PROOFED, HTML_TEST)
        # Make sure there's no yWriter project file present.
        try:
            os.remove(YW7_TEST)
        except:
            pass

    def test_all(self):
        self.assertEqual(proofyw7.run(HTML_TEST),
                         'ERROR: Project "' + YW7_TEST + '" not found.')

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
