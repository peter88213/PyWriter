""" Python unit tests for the pyWriter project.

Test the "proof read" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import zipfile
import pywriter

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

DOCX_FILE = TEST_PROJECT + '.docx'
DOCX_PROOFED_FILE = 'proofed/' + TEST_PROJECT + '.docx'
DOCX_CONTENT = 'word/document.xml'

ODT_FILE = TEST_PROJECT + '.odt'
ODT_PROOFED_FILE = 'proofed/' + TEST_PROJECT + '.odt'
ODT_CONTENT = 'content.xml'

MD_FILE = TEST_PROJECT + '.md'
MD_PROOFED_FILE = 'proofed/' + TEST_PROJECT + '.md'

YW7_FILE = TEST_PROJECT + '.yw7'
YW7_PROOFED_FILE = 'proofed/' + TEST_PROJECT + '.yw7'


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
        os.remove(TEST_EXEC_PATH + DOCX_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + MD_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + ODT_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + YW7_FILE)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + DOCX_CONTENT)
    except:
        pass
    try:
        os.remove(TEST_EXEC_PATH + ODT_CONTENT)
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
            read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + MD_PROOFED_FILE),
            read_file(TEST_DATA_PATH + MD_FILE))

    #@unittest.skip('development')
    def test_exp_to_md(self):
        """ Export yW7 scenes to markdown. """
        pywriter.yw7_to_md(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + MD_FILE)
        # Read .yw7 file and convert xml to markdown.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_FILE))

    #@unittest.skip('development')
    def test_imp_from_md(self):
        """ Import proofed yw7 scenes from markdown . """
        copy_file(TEST_DATA_PATH + MD_PROOFED_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        pywriter.md_to_yw7(TEST_EXEC_PATH + MD_FILE,
                           TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.

    #@unittest.skip('development')
    def test_md_to_docx(self):
        """ Convert markdown to docx. """
        copy_file(TEST_DATA_PATH + MD_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_docx(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + DOCX_FILE)

        with zipfile.ZipFile(TEST_EXEC_PATH + DOCX_FILE, 'r') as myzip:
            myzip.extract(DOCX_CONTENT, TEST_EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCX_CONTENT),
                         read_file(TEST_DATA_PATH + DOCX_CONTENT))

    #@unittest.skip('development')
    def test_docx_to_yw7(self):
        """ Convert docx to markdown. """
        copy_file(TEST_DATA_PATH + DOCX_PROOFED_FILE,
                  TEST_EXEC_PATH + DOCX_FILE)
        pywriter.docx_to_md(TEST_EXEC_PATH + DOCX_FILE,
                            TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_yw7(TEST_EXEC_PATH + MD_FILE,
                           TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.

    #@unittest.skip('development')
    def test_md_to_odt(self):
        """ Convert markdown to odt. """
        copy_file(TEST_DATA_PATH + MD_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_odt(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + ODT_FILE)

        with zipfile.ZipFile(TEST_EXEC_PATH + ODT_FILE, 'r') as myzip:
            myzip.extract(ODT_CONTENT, TEST_EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(TEST_EXEC_PATH + ODT_CONTENT),
                         read_file(TEST_DATA_PATH + ODT_CONTENT))

    #@unittest.skip('development')
    def test_odt_to_yw7(self):
        """ Convert odt to markdown. """
        copy_file(TEST_DATA_PATH + ODT_PROOFED_FILE,
                  TEST_EXEC_PATH + ODT_FILE)
        pywriter.odt_to_md(TEST_EXEC_PATH + ODT_FILE,
                           TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_yw7(TEST_EXEC_PATH + MD_FILE,
                           TEST_EXEC_PATH + YW7_FILE)
        # Convert markdown to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.

    #@unittest.skip('development')
    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
