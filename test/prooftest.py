""" Python unit tests for the yWrestler project.

Test the MS Word docx conversion.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import pywriter

TEST_PROJECT = 'Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

DOCX_FILE = TEST_PROJECT + '.docx'

ODT_FILE = TEST_PROJECT + '.odt'

HTML_FILE = TEST_PROJECT + '.html'
HTML_REFERENCE_FILE = 'original.html'
HTML_PROOFED_FILE = 'proofed.html'

MD_FILE = TEST_PROJECT + '.md'
MD_REFERENCE_FILE = 'original.md'
MD_PROOFED_FILE = 'proofed.md'

YW7_FILE = TEST_PROJECT + '.yw7'
YW7_REFERENCE_FILE = 'original.yw7'
YW7_PROOFED_FILE = 'proofed.yw7'

MD_FILE = TEST_PROJECT + '.md'
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
        os.remove(TEST_EXEC_PATH + HTML_FILE)
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


class NrmOpr(unittest.TestCase):
    """ Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the intermediate
                    markdown file content matches 
                    the corresponding reference string. 
    """

    def setUp(self):
        remove_all_testfiles()
        copy_file(TEST_DATA_PATH + YW7_REFERENCE_FILE,
                  TEST_EXEC_PATH + YW7_FILE)

    def test_data(self):
        """ Verify test data integrity. """
        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW7_REFERENCE_FILE),
            read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + MD_PROOFED_FILE),
            read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + HTML_REFERENCE_FILE),
            read_file(TEST_DATA_PATH + HTML_PROOFED_FILE))

    def test_exp_to_md(self):
        """ Export yW7 scenes to markdown. """
        pywriter.yw7_to_md(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + MD_FILE)
        # Read .yw7 file and convert xml to markdown.
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))

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

    def test_exp_to_html(self):
        """ Export yW7 scenes to html. """
        pywriter.yw7_to_html(
            TEST_EXEC_PATH + YW7_FILE, TEST_EXEC_PATH + HTML_FILE)
        # Read .yw7 file and convert scenes to html.

        self.assertEqual(read_file(TEST_EXEC_PATH + HTML_FILE),
                         read_file(TEST_DATA_PATH + HTML_REFERENCE_FILE))
        # Verify the html file.

    def test_imp_from_html(self):
        """ Import proofed yw7 scenes from html . """
        copy_file(TEST_DATA_PATH + HTML_PROOFED_FILE,
                  TEST_EXEC_PATH + HTML_FILE)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        pywriter.html_to_yw7(TEST_EXEC_PATH + HTML_FILE,
                             TEST_EXEC_PATH + YW7_FILE)
        # Convert document to xml and replace .yw7 file.

        self.assertEqual(read_file(TEST_EXEC_PATH + YW7_FILE),
                         read_file(TEST_DATA_PATH + YW7_PROOFED_FILE))
        # Verify the yw7 project.

    def test_docx(self):
        """ Convert markdown to docx and back to markdown. """
        copy_file(TEST_DATA_PATH + MD_REFERENCE_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_docx(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + DOCX_FILE)
        os.remove(TEST_EXEC_PATH + MD_FILE)
        pywriter.docx_to_md(TEST_EXEC_PATH + DOCX_FILE,
                            TEST_EXEC_PATH + MD_FILE)
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))

    def test_odt(self):
        """ Convert markdown to odt and back to markdown. """
        copy_file(TEST_DATA_PATH + MD_REFERENCE_FILE,
                  TEST_EXEC_PATH + MD_FILE)
        pywriter.md_to_odt(
            TEST_EXEC_PATH + MD_FILE, TEST_EXEC_PATH + ODT_FILE)
        os.remove(TEST_EXEC_PATH + MD_FILE)
        pywriter.odt_to_md(TEST_EXEC_PATH + ODT_FILE,
                           TEST_EXEC_PATH + MD_FILE)
        self.assertEqual(read_file(TEST_EXEC_PATH + MD_FILE),
                         read_file(TEST_DATA_PATH + MD_REFERENCE_FILE))

    def TearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
