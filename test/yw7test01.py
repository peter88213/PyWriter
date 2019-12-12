""" Python unit tests for the yWrestler project.

For further information see https://github.com/peter88213/yWrestler
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import yw7
import yw7read
import yw7write

TEST_PATH = os.getcwd()
TEST_EXEC_PATH = 'yWriter7 Sample/'

YW7_FILE = 'yW7 Sample Project.yw7'
ODT_FILE = 'yW7 Sample Project.odt'


class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation

        Condition: xml import is successful. 
        Expected result: converted string matches the refData string. 
    """

    def setUp(self):
        try:
            os.remove(TEST_EXEC_PATH + ODT_FILE)
        except:
            pass

    def test_markdown(self):
        prjText = yw7read.yw7_to_markdown(
            TEST_EXEC_PATH + YW7_FILE)
        self.assertEqual(prjText, yw7.refData)
        yw7read.markdown_to_odt(prjText, TEST_EXEC_PATH + ODT_FILE)
        self.assertEqual(yw7write.odt_to_markdown(
            TEST_EXEC_PATH + ODT_FILE), yw7.refData)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
