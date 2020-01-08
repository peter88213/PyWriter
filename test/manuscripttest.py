"""Integration tests for the pyWriter project.

Test the "export project" tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.convert.yw7cnv import Yw7Cnv
from pywriter.core.yw7file import Yw7File

from pywriter.edit.manuscript import Manuscript

TEST_PROJECT = 'yw7 Sample Project'

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yw7/'
TEST_DATA_PATH = 'data/'

MANUSCRIPT = TEST_PATH + TEST_PROJECT + '.html'
REFERENCE_MANUSCRIPT = TEST_DATA_PATH + TEST_PROJECT + '_manuscript.html'
EDITED_MANUSCRIPT = TEST_DATA_PATH + 'edit/' + TEST_PROJECT + '_manuscript.html'

YW7_FILE = TEST_PATH + TEST_PROJECT + '.yw7'
YW7_REFERENCE_FILE = TEST_DATA_PATH + TEST_PROJECT + '.yw7'
YW7_EDITED_FILE = TEST_DATA_PATH + 'edit/' + TEST_PROJECT + '.yw7'

with open(YW7_REFERENCE_FILE, 'r') as f:
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
        os.remove(MANUSCRIPT)
    except:
        pass
    try:
        os.remove(YW7_FILE)
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
        copy_file(YW7_REFERENCE_FILE, YW7_FILE)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.
        self.assertNotEqual(
            read_file(YW7_REFERENCE_FILE),
            read_file(YW7_EDITED_FILE))
        self.assertNotEqual(
            read_file(REFERENCE_MANUSCRIPT),
            read_file(EDITED_MANUSCRIPT))

    def test_yw7_to_html(self):
        """Export yW7 scenes to html. """

        yw7File = Yw7File(YW7_FILE)
        documentFile = Manuscript(MANUSCRIPT)
        converter = Yw7Cnv()

        self.assertEqual(converter.yw7_to_document(
            yw7File, documentFile), 'SUCCESS: "' + MANUSCRIPT + '" saved.')
        # Read .yw7 file and convert scenes to html.

        self.assertEqual(read_file(MANUSCRIPT),
                         read_file(REFERENCE_MANUSCRIPT))
        # Verify the html file.

    def test_html_to_yw7(self):
        """Import proofed yw7 scenes from html. """

        copy_file(EDITED_MANUSCRIPT, MANUSCRIPT)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(YW7_FILE)
        documentFile = Manuscript(MANUSCRIPT)
        converter = Yw7Cnv()

        self.assertEqual(converter.document_to_yw7(documentFile, yw7File),
                         'SUCCESS: ' + str(TOTAL_SCENES) + ' Scenes written to "' + YW7_FILE + '".')
        # Convert document to xml and replace .yw7 file.

        self.assertEqual(read_file(YW7_FILE),
                         read_file(YW7_EDITED_FILE))
        # Verify the yw7 project.

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
