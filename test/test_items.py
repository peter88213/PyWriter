"""Integration tests for the pyWriter project.

Test the conversion of the item descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_items import HtmlItems
from pywriter.odt.odt_items import OdtItems
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlItems
    _exportClass = OdtItems


def main():
    unittest.main()

if __name__ == '__main__':
    main()
