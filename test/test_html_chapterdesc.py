"""Integration tests for the pyWriter project.

Test the chapter description conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.converter.yw7cnv import Yw7Cnv
from pywriter.model.yw7file import Yw7File

from pywriter.model.html_chapterdesc import HtmlChapterDesc


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/chapterdesc/'

TEST_DOCUMENT = EXEC_PATH + 'yw7 Sample Project_chapterdesc.html'
REFERENCE_DOCUMENT = DATA_PATH + 'normal.html'
PROOFED_DOCUMENT = DATA_PATH + 'proofed.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'
PROOFED_YW7 = DATA_PATH + 'proofed.yw7'

with open(REFERENCE_YW7, 'r') as f:
    TOTAL_CHAPTERS = f.read().count('<CHAPTER>')


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
        os.remove(TEST_DOCUMENT)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the html 
            file's content matches the reference. 
    """

    def setUp(self):
        remove_all_testfiles()
        copy_file(REFERENCE_YW7,
                  TEST_YW7)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.

        self.assertNotEqual(
            read_file(REFERENCE_YW7),
            read_file(PROOFED_YW7))
        self.assertNotEqual(
            read_file(REFERENCE_DOCUMENT),
            read_file(PROOFED_DOCUMENT))

    def test_yw7_to_chapterdesc(self):
        """Export yW7 chapters to html. """

        yw7File = Yw7File(TEST_YW7)
        documentFile = HtmlChapterDesc(TEST_DOCUMENT)
        converter = Yw7Cnv()

        # Read .yw7 file and convert xml to html.

        self.assertEqual(converter.yw7_to_document(
            yw7File, documentFile), 'SUCCESS: "' + TEST_DOCUMENT + '" saved.')

        self.assertEqual(read_file(TEST_DOCUMENT),
                         read_file(REFERENCE_DOCUMENT))

    def test_chapterdesc_to_yw7(self):
        """Import proofed yw7 chapters from html . """

        copy_file(PROOFED_DOCUMENT,
                  TEST_DOCUMENT)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(TEST_YW7)
        documentFile = HtmlChapterDesc(TEST_DOCUMENT)
        converter = Yw7Cnv()

        # Convert html to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw7(
            documentFile, yw7File), 'SUCCESS: project data written to "' + TEST_YW7 + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
