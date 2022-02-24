"""Provide an abstract test case class for yWriter import and export.

Import/export standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from shutil import copyfile

from pywriter.testcases.helper import read_file
from pywriter.testcases.export_test import ExportTest
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

class ImportExportTest(ExportTest):
    """Test case: Import and export yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None
    
  
    def _set_paths(self):
        super()._set_paths()
        self._TEST_IMP = f'{self._EXEC_PATH}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._REFERENCE_IMP = f'{self._DATA_PATH}normal{self._importClass.EXTENSION}'
        self.PROOFED_IMP = f'{self._DATA_PATH}proofed{self._importClass.EXTENSION}'

    def test_data(self):
        """Verify test data integrity. 

        Initial test data must differ from the "proofed" test data.
        """
        self.assertNotEqual(read_file(self._REFERENCE_YW7),read_file(self._PROOFED_YW7))

    def test_imp_to_yw7(self):
        """Use YwCnv class. """
        copyfile(self.PROOFED_IMP, self._TEST_IMP)
        yw7File = Yw7File(self._TEST_YW7)
        documentFile = self._importClass(self._TEST_IMP)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, yw7File), f'"{ os.path.normpath(self._TEST_YW7)}" written.')
        self.assertEqual(read_file(self._TEST_YW7),read_file(self._PROOFED_YW7))
        self.assertEqual(read_file(self._TEST_YW7_BAK),read_file(self._REFERENCE_YW7))

    def test_imp_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copyfile(self.PROOFED_IMP, self._TEST_IMP)
        converter = Yw7Converter()
        converter.run(self._TEST_IMP)
        self.assertEqual(converter.ui.infoHowText,f'"{ os.path.normpath(self._TEST_YW7)}" written.')
        self.assertEqual(read_file(self._TEST_YW7),read_file(self._PROOFED_YW7))
        self.assertEqual(read_file(self._TEST_YW7_BAK),read_file(self._REFERENCE_YW7))



    def _remove_all_tempfiles(self):
        super()._remove_all_tempfiles()
        
        try:
            os.remove(self._TEST_IMP)
        except:
            pass
        
