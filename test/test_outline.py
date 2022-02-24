"""Integration tests for the pyWriter project.

Test the import of an outline.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_outline import HtmlOutline

importClass = HtmlOutline


from helper import read_file

import os
import unittest
import zipfile
from shutil import copyfile

from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

DATA_PATH = 'data/_outline/'

# From here import-only standard test routines:

EXEC_PATH = 'yw7/'

TEST_IMP = f'{EXEC_PATH}yw7 Sample Project{importClass.SUFFIX}{importClass.EXTENSION}'
REFERENCE_IMP = f'{DATA_PATH}normal{importClass.EXTENSION}'

TEST_YW7 = f'{EXEC_PATH}yw7 Sample Project.yw7'
REFERENCE_YW7 = f'{DATA_PATH}normal.yw7'


def remove_all_tempfiles():

    try:
        os.remove(TEST_IMP)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

    Condition: There is no yw7 file present. 
    Expected result: A new yw7 file matching the reference is created.  
    """

    def setUp(self):

        try:
            os.mkdir(EXEC_PATH)

        except:
            pass

        remove_all_tempfiles()

    def test_imp_to_yw7(self):
        """Use YwCnv class. """
        copyfile(REFERENCE_IMP, TEST_IMP)
        yw7File = Yw7File(TEST_YW7)
        documentFile = importClass(TEST_IMP)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, yw7File), f'"{os.path.normpath(TEST_YW7)}" written.')
        self.assertEqual(read_file(TEST_YW7), read_file(REFERENCE_YW7))

    def test_imp_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copyfile(REFERENCE_IMP, TEST_IMP)
        converter = Yw7Converter()
        converter.run(TEST_IMP)
        self.assertEqual(converter.ui.infoHowText,f'"{os.path.normpath(TEST_YW7)}" written.')
        self.assertEqual(read_file(TEST_YW7),read_file(REFERENCE_YW7))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
