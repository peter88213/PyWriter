""" Python unit tests for the yWrestler project.

Test the proofreading roundtrip using markdown as intermediate format.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
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
YW7_PROOFED_FILE = 'after_proofing.yw7'
ODT_PROOFED_FILE = 'after_proofing.odt'
MD_PROOFED_FILE = 'after_proofing.md'


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
            os.remove(TEST_EXEC_PATH + ODT_FILE)
            os.remove(TEST_EXEC_PATH + MD_FILE)
        except:
            pass
        # Place the correct yw7 project file.
        copy_file(TEST_DATA_PATH + YW7_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_data(self):
        """ Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + MD_PROOFED_FILE),
            read_file(TEST_DATA_PATH + MD_FILE))

    def test_export(self):
        """ Convert yw7 scenes to odt for proofing. """
        yw7read.yw7_to_markdown(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + MD_FILE)
        # Read .yw7 file and convert xml to markdown.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_FILE))

        odtwrite.markdown_to_odt(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + ODT_FILE)
        # Let pandoc convert markdown and write to .odt file.

        odtread.odt_to_markdown(
            TEST_EXEC_PATH + ODT_FILE, TEST_EXEC_PATH + MD_FILE)
        # Verify the ODT file.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_FILE))

    def test_import(self):
        """ Read and replace proofed scenes. """
        copy_file(TEST_DATA_PATH + ODT_PROOFED_FILE,
                  TEST_EXEC_PATH + ODT_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        odtread.odt_to_markdown(
            TEST_EXEC_PATH + ODT_FILE, TEST_EXEC_PATH + MD_FILE)
        # Let pandoc read .odt file and convert to markdown.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_PROOFED_FILE))

        yw7write.md_to_yw7(TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

        yw7read.yw7_to_markdown(TEST_EXEC_PATH + YW7_FILE,
                                # Verify the yw7 file.
                                TEST_EXEC_PATH + MD_FILE)
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_PROOFED_FILE))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
