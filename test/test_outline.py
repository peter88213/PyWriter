"""Integration tests for the pyWriter project.

Test the import of an outline.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_outline import HtmlOutline
from pywriter.testcases.import_test import ImportTest
import unittest


class NrmOpr(ImportTest, unittest.TestCase):
    _importClass = HtmlOutline
    _DATA_PATH = 'data/_outline/'
        
    def test_imp_to_yw7(self):
        """This is needed to identify the source of failure."""
        super().test_imp_to_yw7()
        
    def test_imp_to_yw7_ui(self):
        """This is needed to identify the source of failure."""
        super().test_imp_to_yw7_ui()
        

def main():
    unittest.main()

if __name__ == '__main__':
    main()
