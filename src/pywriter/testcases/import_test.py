"""Provide an abstract test case class for yWriter import.

Import standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from shutil import copyfile

from pywriter.testcases.helper import read_file
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

class ImportTest():
    """Test case: Import yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None
    
  
    def _set_paths(self):
        
        if not hasattr(self, '_DATA_PATH'):
            self._DATA_PATH = f'data/{self._importClass.SUFFIX}/'
            
        self._EXEC_PATH = 'yw7/'
        
        self._TEST_YW7 = f'{self._EXEC_PATH}yw7 Sample Project.yw7'
        self._REFERENCE_YW7 = f'{self._DATA_PATH}normal.yw7'
        
        self._TEST_IMP = f'{self._EXEC_PATH}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._REFERENCE_IMP = f'{self._DATA_PATH}normal{self._importClass.EXTENSION}'

    def setUp(self):
        self._set_paths()

        try:
            os.mkdir(self._EXEC_PATH)

        except:
            pass

        self._remove_all_tempfiles()

    def test_imp_to_yw7(self):
        """Use YwCnv class. """
        copyfile(self._REFERENCE_IMP, self._TEST_IMP)
        yw7File = Yw7File(self._TEST_YW7)
        documentFile = self._importClass(self._TEST_IMP)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, yw7File), f'"{os.path.normpath(self._TEST_YW7)}" written.')
        self.assertEqual(read_file(self._TEST_YW7), read_file(self._REFERENCE_YW7))

    def test_imp_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copyfile(self._REFERENCE_IMP, self._TEST_IMP)
        converter = Yw7Converter()
        converter.run(self._TEST_IMP)
        self.assertEqual(converter.ui.infoHowText,f'"{os.path.normpath(self._TEST_YW7)}" written.')
        self.assertEqual(read_file(self._TEST_YW7),read_file(self._REFERENCE_YW7))

    def tearDown(self):
        self._remove_all_tempfiles()


    def _remove_all_tempfiles(self):
        
        try:
            os.remove(self._TEST_IMP)
        except:
            pass
        
        try:
            os.remove(self._TEST_YW7)
        
        except:
            pass
