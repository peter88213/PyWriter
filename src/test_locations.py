"""Regression test for the pyWriter project.

Test the conversion of the location descriptions.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt_r.odt_r_locations import OdtRLocations
from pywriter.odt_w.odt_w_locations import OdtWLocations
from pywriter.test.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdtRLocations
    _exportClass = OdtWLocations

    # The test methods must be defined here to identify the source of failure.

    def test_yw7_to_exp(self):
        super().test_yw7_to_exp()

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()

    def test_data(self):
        super().test_data()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
