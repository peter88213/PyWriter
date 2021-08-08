"""Integration tests for the PyWriter distributions.

Test the cross reference generation.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.odt.odt_xref import OdtXref

exportClass = OdtXref

from helper import read_file

import os
import unittest
import zipfile
from shutil import copyfile

from pywriter.converter.yw7_converter import Yw7Converter
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File

TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/' + exportClass.SUFFIX + '/'

TEST_ODT = EXEC_PATH + 'yw7 Sample Project' + \
    exportClass.SUFFIX + exportClass.EXTENSION
ODT_CONTENT = 'content.xml'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'
PROOFED_YW7 = DATA_PATH + 'proofed.yw7'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project' + \
    exportClass.SUFFIX + '.html'
REFERENCE_HTML = DATA_PATH + 'normal.html'


def remove_all_tempfiles():
    try:
        os.remove(TEST_HTML)
    except:
        pass
    try:
        os.remove(TEST_ODT)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass
    try:
        os.remove(EXEC_PATH + ODT_CONTENT)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

        Condition: yw7 file is present and read/writeable. 
        Expected result: During the whole process, the html 
            file's content matches the reference. 
    """

    def setUp(self):

        try:
            os.mkdir(EXEC_PATH)

        except:
            pass

        remove_all_tempfiles()
        copyfile(REFERENCE_YW7, TEST_YW7)

    def test_yw7_to_odt(self):
        """Use YwCnv class. """
        yw7File = Yw7File(TEST_YW7)
        documentFile = exportClass(TEST_ODT)
        converter = YwCnv()

        self.assertEqual(converter.convert(
            yw7File, documentFile), 'SUCCESS: "' + os.path.normpath(TEST_ODT) + '" written.')

        with zipfile.ZipFile(TEST_ODT, 'r') as myzip:
            myzip.extract(ODT_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODT_CONTENT),
                         read_file(DATA_PATH + ODT_CONTENT))

    def test_yw7_to_odt_ui(self):
        """Use YwCnvUi class. """
        yw7File = Yw7File(TEST_YW7)

        converter = Yw7Converter()
        kwargs = {'suffix': exportClass.SUFFIX}
        converter.run(TEST_YW7, **kwargs)

        self.assertEqual(converter.ui.infoHowText,
                         'SUCCESS: "' + os.path.normpath(TEST_ODT) + '" written.')

        with zipfile.ZipFile(TEST_ODT, 'r') as myzip:
            myzip.extract(ODT_CONTENT, EXEC_PATH)
            myzip.close

        self.assertEqual(read_file(EXEC_PATH + ODT_CONTENT),
                         read_file(DATA_PATH + ODT_CONTENT))

    def test_html_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copyfile(REFERENCE_HTML, TEST_HTML)
        converter = Yw7Converter()
        converter.run(TEST_HTML)

        self.assertEqual(converter.ui.infoHowText,
                         'ERROR: This document is not meant to be written back.')

        self.assertEqual(read_file(TEST_YW7),
                         read_file(REFERENCE_YW7))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
