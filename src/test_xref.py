"""Regression test for the PyWriter distributions.

Test the cross reference generation.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt_w.odt_w_xref import OdtWXref
from pywriter.test.export_test import ExportTest
import unittest


class NrmOpr(ExportTest, unittest.TestCase):
    _exportClass = OdtWXref

    # The test methods must be defined here to identify the source of failure.

    def test_yw7_to_exp(self):
        super().test_yw7_to_exp()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
