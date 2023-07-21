"""Regression test for the pyWriter project.

Test the conversion of the proofread-manuscript.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt_r.odt_r_proof import OdtRProof
from pywriter.odt_w.odt_w_proof import OdtWProof
from pywriter.test.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdtRProof
    _exportClass = OdtWProof

    # The test methods must be defined here to identify the source of failure.

    def test_yw7_to_exp(self):
        super().test_yw7_to_exp()

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()

    def test_data(self):
        super().test_data()


class ImportFromWord(ImportExportTest, unittest.TestCase):
    """Convert an ODT proofread document saved by MS Word."""
    _importClass = OdtRProof
    _exportClass = OdtWProof

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._prfImpFile = f'{self._dataPath}word{self._importClass.EXTENSION}'
        self._prfYwFile = f'{self._dataPath}word.yw7'

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()

    def _remove_all_tempfiles(self):
        super()._remove_all_tempfiles()

    def test_data(self):
        pass


class ImportFromGoogledocs(ImportExportTest, unittest.TestCase):
    """Convert an ODT proofread document saved by MS Word."""
    _importClass = OdtRProof
    _exportClass = OdtWProof

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._prfImpFile = f'{self._dataPath}googledocs{self._importClass.EXTENSION}'
        self._prfYwFile = f'{self._dataPath}googledocs.yw7'

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()

    def _remove_all_tempfiles(self):
        super()._remove_all_tempfiles()

    def test_data(self):
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
