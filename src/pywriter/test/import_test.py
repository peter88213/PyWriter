"""Provide an abstract test case class for yWriter import.

Import standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from shutil import copyfile

from pywriter.test.helper import read_file
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

class ImportTest():
    """Test case: Import yWriter project.
    
    Public methods:
        setUp() -- set up the test environment.
        test_imp_to_yw7() -- test HTML/CSV import to yWriter, using the YwCnv converter class.
        test_imp_to_yw7_ui() -- test HTML/CSV import to yWriter, using the YwCnvUi converter class.
        tearDown() -- clean up the test execution directory.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None
    
  
    def _init_paths(self):
        """Initialize the test data and execution paths."""  
        
        if not hasattr(self, '_dataPath'):
            self._dataPath = f'data/{self._importClass.SUFFIX}/'
            
        self._execPath = 'yw7/'        
        self._testYwFile = f'{self._execPath}yw7 Sample Project.yw7'
        self._refYwFile = f'{self._dataPath}normal.yw7'        
        self._testImpFile = f'{self._execPath}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._refImpFile = f'{self._dataPath}normal{self._importClass.EXTENSION}'

    def setUp(self):
        """Set up the test environment.
        
        - Initialize the test data and execution paths.
        - Make sure the directory for text execution exists.
        - Remove files that may remain from previous tests.
        """
        self._init_paths()

        try:
            os.mkdir(self._execPath)

        except:
            pass

        self._remove_all_tempfiles()

    def test_imp_to_yw7(self):
        """Test HTML/CSV import to yWriter, using the YwCnv converter class. 
        
        Compare the generated yWriter project file with the reference file.
        """
        copyfile(self._refImpFile, self._testImpFile)
        ywFile = Yw7File(self._testYwFile)
        documentFile = self._importClass(self._testImpFile)
        converter = YwCnv()
        self.assertEqual(converter.convert(documentFile, ywFile), f'"{os.path.normpath(self._testYwFile)}" written.')
        self.assertEqual(read_file(self._testYwFile), read_file(self._refYwFile))

    def test_imp_to_yw7_ui(self):
        """Test HTML/CSV import to yWriter, using the YwCnvUi converter class. 
        
        Compare the generated yWriter project file with the reference file.
        """
        copyfile(self._refImpFile, self._testImpFile)
        converter = Yw7Converter()
        converter.run(self._testImpFile)
        self.assertEqual(converter.ui.infoHowText,f'"{os.path.normpath(self._testYwFile)}" written.')
        self.assertEqual(read_file(self._testYwFile),read_file(self._refYwFile))

    def tearDown(self):
        """Clean up the test execution directory.
        
        This method is called by the unit test framework.
        """
        self._remove_all_tempfiles()

    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        
        try:
            os.remove(self._testImpFile)
        except:
            pass
        
        try:
            os.remove(self._testYwFile)
        
        except:
            pass
