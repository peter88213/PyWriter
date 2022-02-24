"""Integration tests for the pyWriter project.

Test the conversion of the character descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_characters import HtmlCharacters
from pywriter.odt.odt_characters import OdtCharacters
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlCharacters
    _exportClass = OdtCharacters
    
    # The following is needed to identify the source of failure.

    def test_yw7_to_exp(self):
        super().test_yw7_to_exp()
        
    def test_yw7_to_exp_ui(self):
        super().test_yw7_to_exp_ui()
        
    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()
        
    def test_imp_to_yw7_ui(self):
        super().test_imp_to_yw7_ui()
        
    def test_data(self):
        super().test_data()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
