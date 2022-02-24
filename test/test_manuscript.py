"""Integration tests for the pyWriter project.

Test the conversion of the manuscript.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.odt.odt_manuscript import OdtManuscript
from pywriter.testcases.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = HtmlManuscript
    _exportClass = OdtManuscript


def main():
    unittest.main()

if __name__ == '__main__':
    main()
