""" Python unit tests for the yWrestler project.

Test the proofreading roundtrip.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import yw7
import yw7read
import odtwrite
import odtread
import yw7write

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yWriter7 Sample/'
TEST_DATA_PATH = 'data/'

YW7_FILE = 'yW7 Sample Project.yw7'
ODT_FILE = 'yW7 Sample Project.odt'
MD_FILE = 'yW7 Sample Project.md'


def read_file(inputFile):
    with open(inputFile, 'r') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    myData = read_file(inputFile)
    with open(outputFile, 'w') as f:
        f.write(myData)
    return()


class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation

        Condition: xml import is successful. 
        Expected result: converted string matches the refData string. 
    """

    def setUp(self):
        try:
            os.remove(TEST_EXEC_PATH + ODT_FILE)
            os.remove(TEST_EXEC_PATH + MD_FILE)
            os.remove(TEST_EXEC_PATH + YW7_FILE)
        except:
            pass
        # Place the correct yw7 project file.
        copy_file(TEST_DATA_PATH + YW7_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_proofing(self):
        prjText = yw7read.yw7_to_markdown(
            TEST_EXEC_PATH + YW7_FILE)
        # Read .yw7 file and convert xml to markdown.
        self.assertEqual(prjText, yw7.refData)
        yw7read.write_md(prjText, TEST_EXEC_PATH + MD_FILE)
        # Write markdown to .md file.

        prjText = odtwrite.read_md(TEST_EXEC_PATH + MD_FILE)
        # Read markdown from .md file.
        self.assertEqual(prjText, yw7.refData)
        odtwrite.markdown_to_odt(prjText, TEST_EXEC_PATH + ODT_FILE)
        # Let pandoc convert markdown and write to .odt file.

        prjText = odtread.odt_to_markdown(TEST_EXEC_PATH + ODT_FILE)
        # Let pandoc read .odt file and convert to markdown.
        self.assertEqual(prjText, yw7.refData)
        odtread.write_md(prjText, TEST_EXEC_PATH + MD_FILE)
        # Write markdown to .md file.

        prjText = yw7write.read_md(TEST_EXEC_PATH + MD_FILE)
        # Read markdown from .md file.
        self.assertEqual(prjText, yw7.refData)
        yw7write.markdown_to_yw7(prjText, TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

    def tearDown(self):
        try:
            os.remove(TEST_EXEC_PATH + ODT_FILE)
            os.remove(TEST_EXEC_PATH + MD_FILE)
            os.remove(TEST_EXEC_PATH + YW7_FILE)
        except:
            pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
