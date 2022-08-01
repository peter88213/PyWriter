"""Provide an abstract test case class for yWriter import and export.

Import/export standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from shutil import copyfile
from pywriter.pywriter_globals import *
from pywriter.test.helper import read_file
from pywriter.test.export_test import ExportTest
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

UPDATE = False


class ImportExportTest(ExportTest):
    """Test case: Import and export yWriter project.
    
    Public methods:
        test_data() -- verify test data integrity.
        test_imp_to_yw7() -- test HTML/CSV import to yWriter, using the YwCnv converter class.
        test_imp_to_yw7_ui() -- test HTML/CSV import to yWriter, using the YwCnvUi converter class.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._testImpFile = f'{self._execPath}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._refImpFile = f'{self._dataPath}normal{self._importClass.EXTENSION}'
        self._prfImpFile = f'{self._dataPath}proofed{self._importClass.EXTENSION}'

    def test_data(self):
        """Verify test data integrity. 

        Initial test data must differ from the "proofed" test data.
        """
        self.assertNotEqual(read_file(self._refYwFile), read_file(self._prfYwFile))

    def test_imp_to_yw7(self):
        """Test HTML/CSV import to yWriter, using the YwCnv converter class. 
        
        - Overwrite the initial yWriter project file.
        - Compare the generated yWriter project file with the reference file.
        - Compare the yWriter backup with the initial project file.
        """
        copyfile(self._prfImpFile, self._testImpFile)
        ywFile = Yw7File(self._testYwFile)
        documentFile = self._importClass(self._testImpFile)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, ywFile), f'{_("File written")}: "{ os.path.normpath(self._testYwFile)}".')
        if UPDATE:
            copyfile(self._testYwFile, self._prfYwFile)
            copyfile(self._ywBakFile, self._refYwFile)
        self.assertEqual(read_file(self._testYwFile), read_file(self._prfYwFile))
        self.assertEqual(read_file(self._ywBakFile), read_file(self._refYwFile))

    def test_imp_to_yw7_ui(self):
        """Test HTML/CSV import to yWriter, using the YwCnvUi converter class. 
        
        - Overwrite the initial yWriter project file.
        - Compare the generated yWriter project file with the reference file.
        - Compare the yWriter backup with the initial project file.
        """
        copyfile(self._prfImpFile, self._testImpFile)
        converter = Yw7Converter()
        converter.run(self._testImpFile)
        self.assertEqual(converter.ui.infoHowText, f'{_("File written")}: "{ os.path.normpath(self._testYwFile)}".')
        self.assertEqual(read_file(self._testYwFile), read_file(self._prfYwFile))
        self.assertEqual(read_file(self._ywBakFile), read_file(self._refYwFile))

    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        super()._remove_all_tempfiles()
        try:
            os.remove(self._testImpFile)
        except:
            pass

