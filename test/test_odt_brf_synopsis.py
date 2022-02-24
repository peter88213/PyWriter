"""Integration tests for the pyWriter project.

Test the odt brief synopsis.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_brief_synopsis import OdtBriefSynopsis
from pywriter.test.export_test import ExportTest
import unittest


class NrmOpr(ExportTest, unittest.TestCase):
    _exportClass = OdtBriefSynopsis

    # The test methods must be defined here to identify the source of failure.

    def test_yw7_to_exp(self):
        super().test_yw7_to_exp()
        
    def test_yw7_to_exp_ui(self):
        super().test_yw7_to_exp_ui()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
