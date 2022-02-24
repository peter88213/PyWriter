"""Provide an abstract test case class for yWriter export.

Export standard test routines used for regression tests.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile
from shutil import copyfile

from pywriter.test.helper import read_file
from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

class ExportTest():
    """Test case: Import and export yWriter project.
    
    Public methods:
        setUp() -- set up the test environment.
        test_yw7_to_exp() -- test ODF export from yWriter, using the YwCnv converter class.
        test_yw7_to_exp_ui() -- test ODF export from yWriter, using the YwCnvUi converter class.
        tearDown() -- clean up the test execution directory.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _exportClass = None
    
  
    def _init_paths(self):
        """Initialize the test data and execution paths."""  
        
        if not hasattr(self, '_dataPath'):
            self._dataPath = f'data/{self._exportClass.SUFFIX}/'
            
        self._execPath = 'yw7/'       
        self._testExpFile = f'{self._execPath}yw7 Sample Project{self._exportClass.SUFFIX}{self._exportClass.EXTENSION}'
        self._odfCntntFile = 'content.xml'        
        self._testYwFile = f'{self._execPath}yw7 Sample Project.yw7'
        self._ywBakFile = f'{self._testYwFile}.bak'
        self._refYwFile = f'{self._dataPath}normal.yw7'
        self._prfYwFile = f'{self._dataPath}proofed.yw7'
    
    def setUp(self):
        """Set up the test environment.
        
        - Initialize the test data and execution paths.
        - Make sure the directory for text execution exists.
        - Remove files that may remain from previous tests.
        - Create a test yWriter project.
        """
        self._init_paths()
        
        try:
            os.mkdir(self._execPath)

        except:
            pass

        self._remove_all_tempfiles()
        copyfile(self._refYwFile, self._testYwFile)

    def test_yw7_to_exp(self):
        """Test ODF export from yWriter, using the YwCnv converter class. 
        
        Compare the generated content XML file with the reference file.
        """
        ywFile = Yw7File(self._testYwFile)
        documentFile = self._exportClass(self._testExpFile)
        converter = YwCnv()
        self.assertEqual(converter.convert(ywFile, documentFile), f'"{ os.path.normpath(self._testExpFile)}" written.')

        with zipfile.ZipFile(self._testExpFile, 'r') as myzip:
            myzip.extract(self._odfCntntFile, self._execPath)
            myzip.close

        self.assertEqual(read_file(f'{self._execPath}{self._odfCntntFile}'),
                         read_file(f'{self._dataPath}{self._odfCntntFile}'))

    def test_yw7_to_exp_ui(self):
        """Test ODF export from yWriter, using the YwCnvUi converter class. 
        
        Compare the generated content XML file with the reference file.
        """
        converter = Yw7Converter()
        kwargs = {'suffix': self._exportClass.SUFFIX}
        converter.run(self._testYwFile, **kwargs)
        self.assertEqual(converter.ui.infoHowText,f'"{ os.path.normpath(self._testExpFile)}" written.')

        with zipfile.ZipFile(self._testExpFile, 'r') as myzip:
            myzip.extract(self._odfCntntFile, self._execPath)
            myzip.close

        self.assertEqual(read_file(f'{self._execPath}{self._odfCntntFile}'),
                         read_file(f'{self._dataPath}{self._odfCntntFile}'))

    def tearDown(self):
        """Clean up the test execution directory.
        
        This method is called by the unit test framework.
        """
        self._remove_all_tempfiles()


    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        
        try:
            os.remove(self._testExpFile)
        
        except:
            pass
        
        try:
            os.remove(self._testYwFile)
        
        except:
            pass
        
        try:
            os.remove(self._ywBakFile)
        
        except:
            pass
        
        try:
            os.remove(f'{self._execPath}{self._odfCntntFile}')
        
        except:
            pass
    
