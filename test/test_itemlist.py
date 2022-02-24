"""Integration tests for the pyWriter project.

Test the conversion of the item list.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.csv.csv_itemlist import CsvItemList
from pywriter.ods.ods_itemlist import OdsItemList
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = CsvItemList
    _exportClass = OdsItemList


def main():
    unittest.main()

if __name__ == '__main__':
    main()
