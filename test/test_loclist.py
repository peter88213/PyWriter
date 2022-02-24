"""Integration tests for the pyWriter project.

Test the conversion of the location list.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.csv.csv_loclist import CsvLocList
from pywriter.ods.ods_loclist import OdsLocList
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = CsvLocList
    _exportClass = OdsLocList


def main():
    unittest.main()

if __name__ == '__main__':
    main()
