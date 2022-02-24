"""Integration tests for the pyWriter project.

Test the conversion of the location descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_locations import HtmlLocations
from pywriter.odt.odt_locations import OdtLocations

importClass = HtmlLocations
exportClass = OdtLocations

from helper import read_file

import os
import unittest
import zipfile
from shutil import copyfile

from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

# Import/export standard test routines:

DATA_PATH = f'data/{exportClass.SUFFIX}/'
EXEC_PATH = 'yw7/'

TEST_EXP = f'{EXEC_PATH}yw7 Sample Project{exportClass.SUFFIX}{exportClass.EXTENSION}'
ODF_CONTENT = 'content.xml'

TEST_YW7 = f'{EXEC_PATH}yw7 Sample Project.yw7'
TEST_YW7_BAK = f'{TEST_YW7}.bak'
REFERENCE_YW7 = f'{DATA_PATH}normal.yw7'
PROOFED_YW7 = f'{DATA_PATH}proofed.yw7'

TEST_IMP = f'{EXEC_PATH}yw7 Sample Project{importClass.SUFFIX}{importClass.EXTENSION}'
REFERENCE_IMP = f'{DATA_PATH}normal{importClass.EXTENSION}'
PROOFED_IMP = f'{DATA_PATH}proofed{importClass.EXTENSION}'


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
        os.remove(TEST_YW7_BAK)
    except:
        pass
    try:
        os.remove(f'{EXEC_PATH}{ODF_CONTENT}')
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
        copyfile(REFERENCE_YW7, TEST_YW7)

    def test_data(self):
        """Verify test data integrity. 

        Initial test data must differ from the "proofed" test data.
        """
        self.assertNotEqual(read_file(REFERENCE_YW7),read_file(PROOFED_YW7))

    def test_imp_to_yw7(self):
        """Use YwCnv class. """
        copyfile(PROOFED_IMP, TEST_IMP)
        yw7File = Yw7File(TEST_YW7)
        documentFile = importClass(TEST_IMP)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, yw7File), f'"{ os.path.normpath(TEST_YW7)}" written.')
        self.assertEqual(read_file(TEST_YW7),read_file(PROOFED_YW7))
        self.assertEqual(read_file(TEST_YW7_BAK),read_file(REFERENCE_YW7))

    def test_imp_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copyfile(PROOFED_IMP, TEST_IMP)
        converter = Yw7Converter()
        converter.run(TEST_IMP)
        self.assertEqual(converter.ui.infoHowText,f'"{ os.path.normpath(TEST_YW7)}" written.')
        self.assertEqual(read_file(TEST_YW7),read_file(PROOFED_YW7))
        self.assertEqual(read_file(TEST_YW7_BAK),read_file(REFERENCE_YW7))

    def test_yw7_to_exp(self):
        """Use YwCnv class. """
        yw7File = Yw7File(TEST_YW7)
        documentFile = exportClass(TEST_EXP)
        converter = YwCnv()
        self.assertEqual(converter.convert(yw7File, documentFile), f'"{ os.path.normpath(TEST_EXP)}" written.')

        with zipfile.ZipFile(TEST_EXP, 'r') as myzip:
            myzip.extract(ODF_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(f'{EXEC_PATH}{ODF_CONTENT}'),read_file(f'{DATA_PATH}{ODF_CONTENT}'))

    def test_yw7_to_exp_ui(self):
        """Use YwCnvUi class. """
        converter = Yw7Converter()
        kwargs = {'suffix': exportClass.SUFFIX}
        converter.run(TEST_YW7, **kwargs)
        self.assertEqual(converter.ui.infoHowText,f'"{ os.path.normpath(TEST_EXP)}" written.')

        with zipfile.ZipFile(TEST_EXP, 'r') as myzip:
            myzip.extract(ODF_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(f'{EXEC_PATH}{ODF_CONTENT}'),read_file(f'{DATA_PATH}{ODF_CONTENT}'))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
