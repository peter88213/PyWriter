"""Regression test for the pyWriter project.

Test the import of a work in progress.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt_r.odt_r_import import OdtRImport
from pywriter.test.import_test import ImportTest
import unittest


class NrmOpr(ImportTest, unittest.TestCase):
    _importClass = OdtRImport
    _dataPath = '../test/data/_import/'

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_yw7(self):
        super().test_imp_to_yw7()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
