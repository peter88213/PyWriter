"""Provide an abstract test case class for yWriter export.

Export standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile
from shutil import copyfile

from pywriter.testcases.helper import read_file
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

class ExportTest():
    """Test case: Import and export yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _exportClass = None
    
  
    def _set_paths(self):    
        
        if not hasattr(self, '_DATA_PATH'):
            self._DATA_PATH = f'data/{self._exportClass.SUFFIX}/'
            
        self._EXEC_PATH = 'yw7/'
        
        self._TEST_EXP = f'{self._EXEC_PATH}yw7 Sample Project{self._exportClass.SUFFIX}{self._exportClass.EXTENSION}'
        self._ODF_CONTENT = 'content.xml'
        
        self._TEST_YW7 = f'{self._EXEC_PATH}yw7 Sample Project.yw7'
        self._TEST_YW7_BAK = f'{self._TEST_YW7}.bak'
        self._REFERENCE_YW7 = f'{self._DATA_PATH}normal.yw7'
        self._PROOFED_YW7 = f'{self._DATA_PATH}proofed.yw7'
    
    def setUp(self):
        self._set_paths()
        
        try:
            os.mkdir(self._EXEC_PATH)

        except:
            pass

        self._remove_all_tempfiles()
        copyfile(self._REFERENCE_YW7, self._TEST_YW7)

    def test_yw7_to_exp(self):
        """Use YwCnv class. """
        yw7File = Yw7File(self._TEST_YW7)
        documentFile = self._exportClass(self._TEST_EXP)
        converter = YwCnv()
        self.assertEqual(converter.convert(yw7File, documentFile), f'"{ os.path.normpath(self._TEST_EXP)}" written.')

        with zipfile.ZipFile(self._TEST_EXP, 'r') as myzip:
            myzip.extract(self._ODF_CONTENT, self._EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(f'{self._EXEC_PATH}{self._ODF_CONTENT}'),
                         read_file(f'{self._DATA_PATH}{self._ODF_CONTENT}'))

    def test_yw7_to_exp_ui(self):
        """Use YwCnvUi class. """
        converter = Yw7Converter()
        kwargs = {'suffix': self._exportClass.SUFFIX}
        converter.run(self._TEST_YW7, **kwargs)
        self.assertEqual(converter.ui.infoHowText,f'"{ os.path.normpath(self._TEST_EXP)}" written.')

        with zipfile.ZipFile(self._TEST_EXP, 'r') as myzip:
            myzip.extract(self._ODF_CONTENT, self._EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(f'{self._EXEC_PATH}{self._ODF_CONTENT}'),
                         read_file(f'{self._DATA_PATH}{self._ODF_CONTENT}'))

    def tearDown(self):
        self._remove_all_tempfiles()


    def _remove_all_tempfiles(self):
        
        try:
            os.remove(self._TEST_EXP)
        
        except:
            pass
        
        try:
            os.remove(self._TEST_YW7)
        
        except:
            pass
        
        try:
            os.remove(self._TEST_YW7_BAK)
        
        except:
            pass
        
        try:
            os.remove(f'{self._EXEC_PATH}{self._ODF_CONTENT}')
        
        except:
            pass
    

