"""Integration tests for the pyWriter project.

Test the conversion of the character list.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.csv.csv_charlist import CsvCharList
from pywriter.ods.ods_charlist import OdsCharList

importClass = CsvCharList
exportClass = OdsCharList

from helper import read_file, copy_file

import os
import unittest
import zipfile

from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.universal_file_factory import UniversalFileFactory
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/' + exportClass.SUFFIX + '/'

TEST_EXP = EXEC_PATH + 'yw7 Sample Project' + \
    exportClass.SUFFIX + exportClass.EXTENSION
ODF_CONTENT = 'content.xml'

TEST_IMP = EXEC_PATH + 'yw7 Sample Project' + \
    importClass.SUFFIX + importClass.EXTENSION
REFERENCE_IMP = DATA_PATH + 'normal' + importClass.EXTENSION
PROOFED_IMP = DATA_PATH + 'proofed' + importClass.EXTENSION

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'
PROOFED_YW7 = DATA_PATH + 'proofed.yw7'


def remove_all_tempfiles():
    try:
        os.remove(TEST_IMP)
    except:
        pass
    try:
        os.remove(TEST_EXP)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass
    try:
        os.remove(EXEC_PATH + ODF_CONTENT)
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
        copy_file(REFERENCE_YW7, TEST_YW7)

    def test_data(self):
        """Verify test data integrity. """

        # Initial test data must differ from the "proofed" test data.

        self.assertNotEqual(
            read_file(REFERENCE_YW7),
            read_file(PROOFED_YW7))

    def test_imp_to_yw7(self):
        """Use YwCnv class. """
        copy_file(PROOFED_IMP, TEST_IMP)
        yw7File = Yw7File(TEST_YW7)
        documentFile = importClass(TEST_IMP)
        converter = YwCnv()

        self.assertEqual(converter.convert(
            documentFile, yw7File), 'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def test_yw7_to_exp(self):
        """Use YwCnv class. """
        yw7File = Yw7File(TEST_YW7)
        documentFile = exportClass(TEST_EXP)
        converter = YwCnv()

        self.assertEqual(converter.convert(
            yw7File, documentFile), 'SUCCESS: "' + os.path.normpath(TEST_EXP) + '" written.')

        with zipfile.ZipFile(TEST_EXP, 'r') as myzip:
            myzip.extract(ODF_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODF_CONTENT),
                         read_file(DATA_PATH + ODF_CONTENT))

    def test_imp_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copy_file(PROOFED_IMP, TEST_IMP)
        converter = YwCnvUi()
        converter.fileFactory = UniversalFileFactory()
        converter.run(TEST_IMP, importClass.SUFFIX)

        self.assertEqual(converter.ui.infoHowText,
                         'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        self.assertEqual(read_file(TEST_YW7),
                         read_file(PROOFED_YW7))

    def test_yw7_to_exp_ui(self):
        """Use YwCnvUi class. """
        converter = YwCnvUi()
        converter.fileFactory = UniversalFileFactory()
        converter.run(TEST_YW7, exportClass.SUFFIX)

        self.assertEqual(converter.ui.infoHowText,
                         'SUCCESS: "' + os.path.normpath(TEST_EXP) + '" written.')

        with zipfile.ZipFile(TEST_EXP, 'r') as myzip:
            myzip.extract(ODF_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODF_CONTENT),
                         read_file(DATA_PATH + ODF_CONTENT))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
