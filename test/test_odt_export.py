"""Integration tests for the pyWriter project.

Test the odt export.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_export import OdtExport
from pywriter.testcases.export_test import ExportTest
import unittest


class NrmOpr(ExportTest, unittest.TestCase):
    _DATA_PATH = 'data/_odt/'
    _exportClass = OdtExport



def main():
    unittest.main()

if __name__ == '__main__':
    main()
