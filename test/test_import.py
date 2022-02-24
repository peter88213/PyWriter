"""Integration tests for the pyWriter project.

Test the import of a work in progress.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_import import HtmlImport
from pywriter.testcases.import_test import ImportTest
import unittest


class NrmOpr(ImportTest, unittest.TestCase):
    _importClass = HtmlImport
    _DATA_PATH = 'data/_import/'
        
    # The following is needed to identify the source of failure.

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()
        
    def test_imp_to_yw7_ui(self):
        super().test_imp_to_yw7_ui()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
