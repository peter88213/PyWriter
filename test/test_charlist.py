"""Integration tests for the pyWriter project.

Test the csv character list conversion tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File
from pywriter.csv.csv_charlist import CsvCharList


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/' + CsvCharList.SUFFIX + '/'

TEST_CSV = EXEC_PATH + 'yw7 Sample Project' + \
    CsvCharList.SUFFIX + CsvCharList.EXTENSION
REFERENCE_CSV = DATA_PATH + 'normal.csv'
PROOFED_CSV = DATA_PATH + 'proofed.csv'

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


def remove_all_tempfiles():
    try:
        os.remove(TEST_CSV)
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

        try:
            os.mkdir(EXEC_PATH)

        except:
            pass

        remove_all_tempfiles()
        copy_file(REFERENCE_YW7,
                  TEST_YW7)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.

        self.assertNotEqual(
            read_file(REFERENCE_YW7),
            read_file(PROOFED_YW7))
        self.assertNotEqual(
            read_file(REFERENCE_CSV),
            read_file(PROOFED_CSV))

    def test_yw7_to_csv(self):
        """Export yW7 characters to csv. """

        yw7File = Yw7File(TEST_YW7)
        documentFile = CsvCharList(TEST_CSV)
        converter = YwCnv()

        # Read .yw7 file and convert xml to csv.

        self.assertEqual(converter.convert(
            yw7File, documentFile), 'SUCCESS: "' + os.path.normpath(TEST_CSV) + '" written.')

        self.assertEqual(read_file(TEST_CSV),
                         read_file(REFERENCE_CSV))

    def test_csv_to_yw7(self):
        """Import proofed yw7 scenes from csv. """

        copy_file(PROOFED_CSV,
                  TEST_CSV)
        # This substitutes the proof reading process.
        # Note: The yw7 project file is still unchanged.

        yw7File = Yw7File(TEST_YW7)
        documentFile = CsvCharList(TEST_CSV)
        converter = YwCnv()

        # Convert csv to xml and replace .yw7 file.

        self.assertEqual(converter.convert(
            documentFile, yw7File), 'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        # Verify the yw7 project.

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
