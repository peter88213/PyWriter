"""Integration tests for the pyWriter project.

Test the conversion of the part descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_partdesc import HtmlPartDesc
from pywriter.odt.odt_partdesc import OdtPartDesc
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlPartDesc
    _exportClass = OdtPartDesc

    def test_yw7_to_exp(self):
        """This is needed to identify the source of failure."""
        super().test_yw7_to_exp()
        
    def test_yw7_to_exp_ui(self):
        """This is needed to identify the source of failure."""
        super().test_yw7_to_exp_ui()
        
    def test_imp_to_yw7(self):
        """This is needed to identify the source of failure."""
        super().test_imp_to_yw7()
        
    def test_imp_to_yw7_ui(self):
        """This is needed to identify the source of failure."""
        super().test_imp_to_yw7_ui()
        
    def test_data(self):
        """This is needed to identify the source of failure."""
        super().test_data()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
