"""Integration tests for the pyWriter project.

Test the odt export.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_export import OdtExport

exportClass = OdtExport

from helper import read_file

import os
import unittest
import zipfile
from shutil import copyfile

from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

DATA_PATH = 'data/_odt/'

# From here export-only standard test routines:

EXEC_PATH = 'yw7/'

TEST_EXP = f'{EXEC_PATH}yw7 Sample Project{exportClass.SUFFIX}{exportClass.EXTENSION}'
ODF_CONTENT = 'content.xml'

TEST_YW7 = f'{EXEC_PATH}yw7 Sample Project.yw7'
TEST_YW7_BAK = f'{TEST_YW7}.bak'
REFERENCE_YW7 = f'{DATA_PATH}normal.yw7'
PROOFED_YW7 = f'{DATA_PATH}proofed.yw7'

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

    def test_yw7_to_exp(self):
        """Use YwCnv class. """
        yw7File = Yw7File(TEST_YW7)
        documentFile = exportClass(TEST_EXP)
        converter = YwCnv()
        self.assertEqual(converter.convert(yw7File, documentFile), f'"{ os.path.normpath(TEST_EXP)}" written.')

        with zipfile.ZipFile(TEST_EXP, 'r') as myzip:
            myzip.extract(ODF_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(f'{EXEC_PATH}{ODF_CONTENT}'), read_file(f'{DATA_PATH}{ODF_CONTENT}'))

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
