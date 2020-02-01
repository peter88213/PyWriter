"""Integration tests for the pyWriter project.

Test the csv scenes list conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.converter.yw7cnv import Yw7Cnv
from pywriter.model.yw7file import Yw7File

from pywriter.model.plotlist import PlotList


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/plotlist/'

TEST_DOCUMENT = EXEC_PATH + 'yw7 Sample Project_plot.csv'
REFERENCE_DOCUMENT = DATA_PATH + 'normal.csv'
PROOFED_DOCUMENT = DATA_PATH + 'proofed.csv'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'
PROOFED_YW7 = DATA_PATH + 'proofed.yw7'

with open(REFERENCE_YW7, 'r') as f:
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

    @unittest.skip('l')
    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.

        self.assertNotEqual(
            read_file(REFERENCE_YW7),
            read_file(PROOFED_YW7))
        self.assertNotEqual(
            read_file(REFERENCE_DOCUMENT),
            read_file(PROOFED_DOCUMENT))

    def test_yw7_to_csv(self):
        """Export yW7 scenes to csv. """

        yw7File = Yw7File(TEST_YW7)
        documentFile = PlotList(TEST_DOCUMENT)
        converter = Yw7Cnv()

        # Read .yw7 file and convert xml to csv.

        self.assertEqual(converter.yw7_to_document(
            yw7File, documentFile), 'SUCCESS: "' + TEST_DOCUMENT + '" saved.')

        self.assertEqual(read_file(TEST_DOCUMENT),
                         read_file(REFERENCE_DOCUMENT))

    def test_csv_to_yw7(self):
        """Import proofed yw7 scenes from csv. """

        copy_file(PROOFED_DOCUMENT,
                  TEST_DOCUMENT)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(TEST_YW7)
        documentFile = PlotList(TEST_DOCUMENT)
        converter = Yw7Cnv()

        # Convert csv to xml and replace .yw7 file.

        self.assertEqual(converter.document_to_yw7(documentFile, yw7File), 'SUCCESS: ' + str(
            TOTAL_SCENES) + ' Scenes written to "' + TEST_YW7 + '".')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
