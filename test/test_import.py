"""Integration tests for the pyWriter project.

Test the import of a work in progress.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.html.html_import import HtmlImport

importClass = HtmlImport

from helper import read_file, copy_file

import os
import unittest
import zipfile

from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.universal_file_factory import UniversalFileFactory
from pywriter.converter.yw_cnv import YwCnv
from pywriter.yw.yw7_file import Yw7File
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.yw_project_creator import YwProjectCreator


DATA_PATH = 'data/_import/'
TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'

TEST_HTML = EXEC_PATH + 'yw7 Sample Project.html'
REFERENCE_HTML = DATA_PATH + 'normal.html'

TEST_YW7 = EXEC_PATH + 'yw7 Sample Project.yw7'
REFERENCE_YW7 = DATA_PATH + 'normal.yw7'


def remove_all_tempfiles():

    try:
        os.remove(TEST_HTML)
    except:
        pass
    try:
        os.remove(TEST_YW7)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation

    Condition: There is no yw7 file present. 
    Expected result: A new yw7 file matching the reference is created.  
    """

    def setUp(self):

        try:
            os.mkdir(EXEC_PATH)

        except:
            pass

        remove_all_tempfiles()

    def test_html_to_yw7(self):
        """Use YwCnv class. """
        copy_file(REFERENCE_HTML, TEST_HTML)
        yw7File = Yw7File(TEST_YW7)
        yw7File.ywTreeBuilder = Yw7TreeCreator()
        yw7File.ywProjectMerger = YwProjectCreator()
        documentFile = importClass(TEST_HTML)
        converter = YwCnv()

        self.assertEqual(converter.convert(
            documentFile, yw7File), 'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        self.assertEqual(read_file(TEST_YW7),
                         read_file(REFERENCE_YW7))

    def test_html_to_yw7_ui(self):
        """Use YwCnvUi class. """
        copy_file(REFERENCE_HTML, TEST_HTML)
        converter = YwCnvUi()
        converter.fileFactory = UniversalFileFactory()
        converter.run(TEST_HTML, importClass.SUFFIX)

        self.assertEqual(converter.ui.infoHowText,
                         'SUCCESS: "' + os.path.normpath(TEST_YW7) + '" written.')

        self.assertEqual(read_file(TEST_YW7),
                         read_file(REFERENCE_YW7))

    def tearDown(self):
        remove_all_tempfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
