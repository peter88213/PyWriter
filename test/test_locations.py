"""Integration tests for the pyWriter project.

Test the conversion of the location descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_locations import HtmlLocations
from pywriter.odt.odt_locations import OdtLocations
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlLocations
    _exportClass = OdtLocations


def main():
    unittest.main()

if __name__ == '__main__':
    main()
