"""Integration tests for the pyWriter project.

Test the conversion of the scene descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_scenedesc import HtmlSceneDesc
from pywriter.odt.odt_scenedesc import OdtSceneDesc
from pywriter.test.import_export_test import ImportExportTest
import unittest

class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlSceneDesc
    _exportClass = OdtSceneDesc

    # The test methods must be defined here to identify the source of failure.

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
