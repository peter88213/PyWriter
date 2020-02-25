""" Python unit tests for the yW2OO project.

Test suite for yw2oo.py.

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import zipfile

import yw2oo


# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd()
TEST_DATA_PATH = 'data/yw2oo/'
TEST_EXEC_PATH = 'yw7/'

# To be placed in TEST_DATA_PATH:

# Test data
YW7_TEST = TEST_EXEC_PATH + 'yWriter Sample Project.yw7'
ODT_TEST = 'yWriter Sample Project.odt'

DOCUMENT_CONTENT = 'content.xml'
DOCUMENT_META = 'meta.xml'
DOCUMENT_STYLES = 'styles.xml'

YW7_NORMAL = TEST_DATA_PATH + 'normal.yw7'
DOC_NORMAL = TEST_DATA_PATH + 'normal.odt'


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
        os.remove(TEST_EXEC_PATH + DOCUMENT_STYLES)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCUMENT_CONTENT)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + ODT_TEST)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):

        try:
            os.remove(TEST_EXEC_PATH + ODT_TEST)
        except:
            pass
        copy_file(YW7_NORMAL, YW7_TEST)

    def test_yw2oo(self):
        os.chdir(TEST_EXEC_PATH)
        self.assertEqual(yw2oo.main(), 'SUCCESS: "' + ODT_TEST + '" saved.')
        os.chdir(TEST_PATH)

        with zipfile.ZipFile(TEST_EXEC_PATH + ODT_TEST, 'r') as myzip:
            myzip.extract(DOCUMENT_CONTENT, TEST_EXEC_PATH)
            myzip.extract(DOCUMENT_STYLES, TEST_EXEC_PATH)

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_CONTENT),
                         read_file(TEST_DATA_PATH + DOCUMENT_CONTENT))
        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_STYLES),
                         read_file(TEST_DATA_PATH + DOCUMENT_STYLES))

    def tearDown(self):
        remove_all_testfiles()


class NoProjectFile(unittest.TestCase):
    """Test case: yWriter project file is not present."""

    def setUp(self):
        # Make sure there's no yWriter project file present.
        try:
            os.remove(YW7_TEST)
        except:
            pass

    def test_all(self):
        """ Test both yw2oo and sceti. """
        self.assertEqual(yw2oo.main(), 'ERROR: No yWriter 7 project found.')

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
