"""Integration tests for the PyWriter distributions.

Test the "proof read" scripts. 

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest
import zipfile
import proofdocx
import proofodt
import proofhtml

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = '../test/'
EXEC_PATH = TEST_PATH + 'yw7/'
DATA_PATH = TEST_PATH + 'data/'

TEST_DOCX = EXEC_PATH + 'yw7 Sample Project.docx'
DOCX_CONTENT = 'word/document.xml'
PROOFED_DOCX = DATA_PATH + 'office/proofed.docx'

TEST_ODT = EXEC_PATH + 'yw7 Sample Project.odt'
ODT_CONTENT = 'content.xml'
PROOFED_ODT = DATA_PATH + 'office/proofed.odt'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
REFERENCE_HTML = DATA_PATH + 'html/normal.html'
PROOFED_HTML = DATA_PATH + 'html/proofed.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
OFFICE_REF_YW7 = DATA_PATH + 'office/normal.yw7'
OFFICE_PROOFED_YW7 = DATA_PATH + 'office/proofed.yw7'
HTML_REF_YW7 = DATA_PATH + 'html/normal.yw7'
HTML_PROOFED_YW7 = DATA_PATH + 'html/proofed.yw7'


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
        os.remove(TEST_DOCX)
    except:
        pass
    try:
        os.remove(TEST_ODT)
    except:
        pass
    try:
        os.remove(TEST_HTML)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass
    try:
        os.remove(EXEC_PATH + DOCX_CONTENT)
    except:
        pass
    try:
        os.remove(EXEC_PATH + ODT_CONTENT)
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
        copy_file(OFFICE_REF_YW7, TEST_YW7)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(OFFICE_REF_YW7),
            read_file(OFFICE_PROOFED_YW7))

    def test_yw7_to_docx(self):
        """Convert markdown to docx. """

        proofdocx.run(TEST_YW7, True)

        with zipfile.ZipFile(TEST_DOCX, 'r') as myzip:
            myzip.extract(DOCX_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + DOCX_CONTENT),
                         read_file(DATA_PATH + 'office/' + DOCX_CONTENT))

    def test_docx_to_yw7(self):
        """Convert docx to markdown. """

        copy_file(PROOFED_DOCX, TEST_DOCX)
        proofdocx.run(TEST_DOCX, True)

        self.assertEqual(read_file(TEST_YW7),
                         read_file(OFFICE_PROOFED_YW7))

    def test_yw7_to_odt(self):
        """Convert markdown to odt. """

        proofodt.run(TEST_YW7, True)

        with zipfile.ZipFile(TEST_ODT, 'r') as myzip:
            myzip.extract(ODT_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODT_CONTENT),
                         read_file(DATA_PATH + 'office/' + ODT_CONTENT))

    def test_odt_to_yw7(self):
        """Convert odt to markdown. """

        copy_file(PROOFED_ODT, TEST_ODT)
        proofodt.run(TEST_ODT, True)

        self.assertEqual(read_file(TEST_YW7),
                         read_file(OFFICE_PROOFED_YW7))

    def test_yw7_to_html(self):
        """Convert markdown to html. """

        proofhtml.run(TEST_YW7, True)

        self.assertEqual(read_file(TEST_HTML),
                         read_file(REFERENCE_HTML))

    def test_html_to_yw7(self):
        """Convert html to markdown. """

        copy_file(PROOFED_HTML, TEST_HTML)
        proofhtml.run(TEST_HTML, True)

        self.assertEqual(read_file(TEST_YW7),
                         read_file(HTML_PROOFED_YW7))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
